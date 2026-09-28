
"""
Rule-based generation of Formal Term Assessment Reports.

Reads submitted assessment data and assembles a structured report.
Does not modify assessments, save reports or publish results.
"""

from django.core.exceptions import ValidationError

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction

from profiles.models import (
    SUBSKILLS,
    StudentSubSkillAssessment,
    StudentTermAssessment,
    StudentTermAssessmentReport,
)

from .term_assessment_report_content import (
    RATING_INTERPRETATIONS,
    SUBSKILL_RECOMMENDATIONS,
    SUBSKILL_NARRATIVES,
    NARRATIVE_RATING_LANGUAGE,
    SUBSKILL_DEVELOPMENT_NARRATIVES,
    SKILL_CONSOLIDATION_NARRATIVES,
    SKILL_SATISFACTORY_NARRATIVES,
    SUBSKILL_NEXT_TERM_FOCUS,
)


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

MAX_PRIORITIES = 3

RATING = StudentSubSkillAssessment.Rating
SCORES = StudentSubSkillAssessment.SCORE_BY_RATING

SKILL_LABELS = {
    "speaking": "Speaking",
    "reading": "Reading",
    "listening": "Listening",
    "writing": "Writing",
}

SUBSKILL_LABELS = {
    skill: dict(subskills)
    for skill, subskills in SUBSKILLS.items()
}


# ---------------------------------------------------------
# VALIDATION AND DATA COLLECTION
# ---------------------------------------------------------

def get_report_assessment_data(assessment):
    """Return validated, ordered data from a submitted assessment."""

    if assessment.status != StudentTermAssessment.Status.SUBMITTED:
        raise ValidationError("Only submitted assessments can generate reports.")

    if assessment.overall_score is None:
        raise ValidationError("The assessment has no overall score.")

    snapshots = list(
        assessment.skill_snapshots.prefetch_related("subskill_assessments")
    )

    snapshot_map = {snapshot.skill: snapshot for snapshot in snapshots}

    if len(snapshots) != len(SUBSKILLS) or set(snapshot_map) != set(SUBSKILLS):
        raise ValidationError("The assessment must contain all four skills.")

    skills = []
    subskills = []

    for skill, expected_subskills in SUBSKILLS.items():
        snapshot = snapshot_map[skill]

        if snapshot.score is None:
            raise ValidationError(f"{SKILL_LABELS[skill]} has no calculated score.")

        records = list(snapshot.subskill_assessments.all())
        record_map = {record.subskill: record for record in records}
        expected_keys = {key for key, _ in expected_subskills}

        if len(records) != len(expected_keys) or set(record_map) != expected_keys:
            raise ValidationError(
                f"{SKILL_LABELS[skill]} has incomplete subskill records."
            )

        skills.append({
            "key": skill,
            "label": SKILL_LABELS[skill],
            "score": snapshot.score,
        })

        for subskill, label in expected_subskills:
            record = record_map[subskill]

            if record.rating not in SCORES:
                raise ValidationError(
                    f"{SKILL_LABELS[skill]}: {label} has an invalid or missing rating."
                )

            if subskill not in SUBSKILL_RECOMMENDATIONS.get(skill, {}):
                raise ValidationError(
                    f"No report recommendation exists for {skill}: {subskill}."
                )

            subskills.append({
                "skill": skill,
                "skill_label": SKILL_LABELS[skill],
                "subskill": subskill,
                "label": label,
                "rating": record.rating,
                "rating_label": record.get_rating_display(),
                "score": SCORES[record.rating],
                "recommendation": SUBSKILL_RECOMMENDATIONS[skill][subskill],
            })

    return skills, subskills



# ---------------------------------------------------------
# PERFORMANCE SUMMARY
# ---------------------------------------------------------

def join_narrative_items(items):
    """Join report expressions using natural English punctuation."""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])} and {items[-1]}"


def build_skill_performance_summary(skill, items, learner_name):
    """Describe every recorded subskill within one language skill."""

    rating_order = (
        RATING.STRONG,
        RATING.CONFIDENT,
        RATING.SATISFACTORY,
        RATING.DEVELOPING,
        RATING.NEEDS_WORK,
    )

    groups = {rating: [] for rating in rating_order}

    for item in items:
        expression = SUBSKILL_NARRATIVES[skill][item["subskill"]]
        groups[item["rating"]].append(expression)

    sentences = []

    openings = {
        RATING.STRONG: f"{learner_name} demonstrates strong ability in",
        RATING.CONFIDENT: f"{learner_name} demonstrates confidence in",
        RATING.SATISFACTORY: f"{learner_name} demonstrates satisfactory ability in",
        RATING.DEVELOPING: f"{learner_name} demonstrates developing ability in",
        RATING.NEEDS_WORK: f"{learner_name} currently shows limited ability in",
    }

    for rating in rating_order:
        expressions = groups[rating]

        if expressions:
            sentences.append(
                f"{openings[rating]} {join_narrative_items(expressions)}."
            )

    return " ".join(sentences)


def build_performance_summary(subskills, learner_name):
    """
    Generate four skill-specific narrative paragraphs.

    Every assessed subskill contributes to its corresponding paragraph.
    Ratings and numerical scores are not modified.
    """

    summary = {}

    for skill in SKILL_LABELS:
        skill_items = [
            item for item in subskills
            if item["skill"] == skill
        ]

        if len(skill_items) != len(SUBSKILLS[skill]):
            raise ValidationError(
                f"Cannot generate a complete {SKILL_LABELS[skill]} summary."
            )

        summary[skill] = build_skill_performance_summary(
            skill,
            skill_items,
            learner_name,
        )

    return summary



# ---------------------------------------------------------
# SKILL-SPECIFIC DEVELOPMENT PRIORITIES
# ---------------------------------------------------------

def build_development_priorities(subskills):
    """
    Generate a development paragraph for each language skill.

    Needs Work / Developing: targeted development.
    Satisfactory: consolidation and further improvement.
    Confident / Strong: consolidation and extension.
    """
    priorities = {}

    for skill in SKILL_LABELS:
        skill_items = [
            item for item in subskills
            if item["skill"] == skill
        ]

        if len(skill_items) != len(SUBSKILLS[skill]):
            raise ValidationError(
                f"Cannot generate complete {SKILL_LABELS[skill]} development priorities."
            )

        needs_work = [
            item for item in skill_items
            if item["rating"] == RATING.NEEDS_WORK
        ]

        developing = [
            item for item in skill_items
            if item["rating"] == RATING.DEVELOPING
        ]

        satisfactory = [
            item for item in skill_items
            if item["rating"] == RATING.SATISFACTORY
        ]

        sentences = []

        # Targeted development
        for item in needs_work + developing:
            sentences.append(
                SUBSKILL_DEVELOPMENT_NARRATIVES[skill][item["subskill"]]
            )

        # Satisfactory: acknowledge achievement while
        # identifying specific opportunities for improvement.
        if satisfactory:
            if not needs_work and not developing:
                sentences.append(
                    SKILL_SATISFACTORY_NARRATIVES[skill]
                )
            else:
                expressions = [
                    SUBSKILL_NARRATIVES[skill][item["subskill"]]
                    for item in satisfactory
                ]

                sentences.append(
                    "Further consolidation and improvement are encouraged in "
                    f"{join_narrative_items(expressions)}."
                )

            for item in satisfactory:
                sentences.append(
                    SUBSKILL_RECOMMENDATIONS[skill][item["subskill"]]
                )

        # No development ratings and no Satisfactory:
        # all subskills are Confident or Strong.
        if not sentences:
            sentences.append(
                SKILL_CONSOLIDATION_NARRATIVES[skill]
            )

        priorities[skill] = " ".join(sentences)

    return priorities


# ---------------------------------------------------------
# DEVELOPMENT PRIORITIES
# ---------------------------------------------------------

def select_development_priorities(subskills):
    """
    Select up to three priorities.

    Priority order:
    1. Focus areas
    2. Developing
    3. Satisfactory, for consolidation
    4. Confident in / Key strengths, for extension

    Equal ratings retain the existing SUBSKILLS order.
    """

    ordered = sorted(subskills, key=lambda item: item["score"])

    development = [
        item for item in ordered
        if item["rating"] in (RATING.NEEDS_WORK, RATING.DEVELOPING)
    ]

    if development:
        selected = development[:MAX_PRIORITIES]
        focus_type = "development"
    else:
        selected = ordered[:MAX_PRIORITIES]
        focus_type = "consolidation"

    priorities = []

    for item in selected:
        priorities.append({
            **item,
            "focus_type": focus_type,
            "interpretation": RATING_INTERPRETATIONS[item["rating"]],
        })

    return priorities


# ---------------------------------------------------------
# NEXT-TERM FOCUS
# ---------------------------------------------------------


# ---------------------------------------------------------
# NEXT-TERM FOCUS — NARRATIVE GENERATION
# ---------------------------------------------------------

def build_next_term_focus(priorities):
    """
    Generate a natural-language learning direction from
    the three selected priorities.

    Preserve the existing priority selection and distinguish
    targeted development from consolidation.
    """
    if not priorities:
        return (
            "Continued practice across all four language skills is encouraged "
            "to consolidate existing abilities and support further progress."
        )

    objectives = [
        SUBSKILL_NEXT_TERM_FOCUS[item["skill"]][item["subskill"]]
        for item in priorities
    ]

    focus = join_narrative_items(objectives)

    has_development_priorities = any(
        item["focus_type"] != "consolidation"
        for item in priorities
    )

    if has_development_priorities:
        return (
            f"The next learning period should focus on {focus}. "
            "Targeted practice in these areas will support continued progress "
            "towards more confident, accurate and effective communication "
            "in English."
        )

    return (
        f"The next learning period should focus on {focus}. "
        "Continued practice in these areas is encouraged to consolidate "
        "existing abilities, extend confidence and support further progress "
        "in English."
    )


# ---------------------------------------------------------
# COMPLETE REPORT GENERATION
# ---------------------------------------------------------

def generate_term_assessment_report(assessment):
    """
    Assemble a report from a submitted Formal Term Assessment.

    Returns a structured dictionary.
    Does not save, regenerate or publish a report record.
    """

    skills, subskills = get_report_assessment_data(assessment)

    priorities = select_development_priorities(subskills)

    student = assessment.enrollment.student

    learner_name = student.first_name.strip() or student.get_full_name() or student.username

    return {
        "assessment_id": assessment.pk,
        "learner": student.get_full_name() or student.username,
        "course": str(assessment.enrollment.course),
        "term_label": assessment.term_label,
        "assessment_date": assessment.assessment_date,
        "teacher": (
            assessment.teacher.get_full_name() or assessment.teacher.username
            if assessment.teacher_id else None
        ),
        "overall_score": assessment.overall_score,
        "skills": skills,
        "performance_summary": build_performance_summary(subskills, learner_name),
        "development_priorities": build_development_priorities(subskills),
        "next_term_priorities": priorities,
        "next_term_focus": build_next_term_focus(priorities),
    }




# ---------------------------------------------------------
# PERSISTENT REPORT CREATION
# ---------------------------------------------------------

@transaction.atomic
def create_term_assessment_report(assessment, generated_by):
    """
    Generate and persist one report for a submitted assessment.

    Must be called explicitly by an authorised teacher-facing action.

    Existing reports are never regenerated or overwritten.
    """

    if generated_by is None or not generated_by.pk:
        raise ValidationError("A report must have a valid generating user.")

    # Lock the assessment during report creation.
    assessment = StudentTermAssessment.objects.select_for_update().get(
        pk=assessment.pk
    )

    if assessment.status != StudentTermAssessment.Status.SUBMITTED:
        raise ValidationError(
            "Only submitted assessments can have generated reports."
        )

    if StudentTermAssessmentReport.objects.filter(
        assessment=assessment
    ).exists():
        raise ValidationError(
            "A report has already been generated for this assessment."
        )

    # Generate the report from the submitted academic records.
    report_data = generate_term_assessment_report(assessment)

    # Convert Decimal and date values into JSON-compatible values.
    # Decimal scores are preserved as strings, avoiding float conversion.
    report_content = json.loads(
        json.dumps(report_data, cls=DjangoJSONEncoder)
    )

    return StudentTermAssessmentReport.objects.create(
        assessment=assessment,
        content=report_content,
        generated_by=generated_by,
    )
