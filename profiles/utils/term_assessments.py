from django.db import transaction

from django.core.exceptions import ValidationError
from django.utils import timezone

from profiles.models import (
    SUBSKILLS,
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    StudentTermAssessment,
    StudentSkillTermSnapshot,
    StudentTermSubSkillAssessment,
)


@transaction.atomic
def get_or_create_term_assessment_draft(enrollment, term_label):
    """
    Create a formal Term Assessment draft for one enrollment.

    Copies available ongoing subskill ratings once.
    Existing assessments are returned without modification.
    """

    term_label = term_label.strip()

    if not term_label:
        raise ValueError("A term label is required.")

    assessment, created = StudentTermAssessment.objects.get_or_create(
        enrollment=enrollment,
        term_label=term_label,
        defaults={"status": StudentTermAssessment.Status.DRAFT},
    )

    if not created:
        return assessment, False

    # Read the learner's current ongoing assessments.
    ongoing_assessments = (
        StudentSkillAssessment.objects
        .filter(student=enrollment.student, course=enrollment.course)
        .prefetch_related("subskill_assessments")
    )

    ratings = {
        (assessment.skill, subskill.subskill): subskill.rating
        for assessment in ongoing_assessments
        for subskill in assessment.subskill_assessments.all()
    }

    # Create the four independent formal skill records.
    for skill, subskills in SUBSKILLS.items():
        skill_snapshot = StudentSkillTermSnapshot.objects.create(
            term_assessment=assessment,
            skill=skill,
        )

        # Create every expected subskill, including unrated ones.
        StudentTermSubSkillAssessment.objects.bulk_create([
            StudentTermSubSkillAssessment(
                skill_snapshot=skill_snapshot,
                subskill=subskill,
                rating=ratings.get((skill, subskill)),
            )
            for subskill, _ in subskills
        ])

    return assessment, True


@transaction.atomic
def submit_term_assessment(assessment, teacher):
    """
    Validate and submit a formal Term Assessment.

    All four skills and all 14 subskills must be present and rated.
    Final scores are stored independently of ongoing assessments.
    """
    assessment = (
        StudentTermAssessment.objects
        .select_for_update()
        .get(pk=assessment.pk)
    )

    if assessment.status != StudentTermAssessment.Status.DRAFT:
        raise ValidationError("Only draft assessments can be submitted.")

    if teacher is None or not teacher.pk:
        raise ValidationError("A teacher is required to submit an assessment.")

    snapshots = list(
        assessment.skill_snapshots
        .prefetch_related("subskill_assessments")
    )

    expected_skills = set(SUBSKILLS)

    if len(snapshots) != len(expected_skills):
        raise ValidationError("The assessment must contain all four skills.")

    if {snapshot.skill for snapshot in snapshots} != expected_skills:
        raise ValidationError("The assessment contains an invalid skill structure.")

    skill_scores = []

    for snapshot in snapshots:
        subskills = list(snapshot.subskill_assessments.all())
        expected_subskills = {
            subskill for subskill, _ in SUBSKILLS[snapshot.skill]
        }

        if (
            len(subskills) != len(expected_subskills)
            or {item.subskill for item in subskills} != expected_subskills
        ):
            raise ValidationError(
                f"{snapshot.get_skill_display()} has an incomplete subskill structure."
            )

        if any(item.score is None for item in subskills):
            raise ValidationError(
                f"All {snapshot.get_skill_display()} subskills must be rated."
            )

        score = snapshot.calculated_score

        if score is None:
            raise ValidationError("A skill score could not be calculated.")

        skill_scores.append((snapshot, score))

    # Validation has completed successfully. Persist the final results.
    for snapshot, score in skill_scores:
        snapshot.score = score
        snapshot.save(update_fields=["score"])

    assessment.overall_score = assessment.calculated_overall_score
    assessment.teacher = teacher
    assessment.assessment_date = assessment.assessment_date or timezone.localdate()
    assessment.submitted_at = timezone.now()
    assessment.status = StudentTermAssessment.Status.SUBMITTED

    assessment.save(update_fields=[
        "overall_score",
        "teacher",
        "assessment_date",
        "submitted_at",
        "status",
        "updated_at",
    ])

    return assessment

@transaction.atomic
def update_term_subskill_rating(subskill_assessment, rating):
    """Update an independent formal rating while its assessment is a draft."""
    assessment = (
        StudentTermAssessment.objects
        .select_for_update()
        .get(pk=subskill_assessment.skill_snapshot.term_assessment_id)
    )

    if assessment.status != StudentTermAssessment.Status.DRAFT:
        raise ValidationError("Only draft assessment ratings can be edited.")

    valid_ratings = {
        choice.value
        for choice in StudentSubSkillAssessment.Rating
    }

    if rating not in valid_ratings and rating is not None:
        raise ValidationError("Invalid assessment rating.")

    subskill = StudentTermSubSkillAssessment.objects.get(
        pk=subskill_assessment.pk,
        skill_snapshot__term_assessment=assessment,
    )

    subskill.rating = rating
    subskill.save(update_fields=["rating", "updated_at"])

    return subskill