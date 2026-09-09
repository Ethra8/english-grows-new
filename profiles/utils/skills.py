from profiles.models import SUBSKILLS, StudentSkillAssessment


SKILL_ICONS = {
    "speaking": "fa-solid fa-microphone",
    "reading": "fa-solid fa-book-open",
    "writing": "fa-solid fa-pen",
    "listening": "fa-solid fa-headphones",
}


SKILL_AREAS = [
    ("listening", "Listening"),
    ("reading", "Reading"),
    ("speaking", "Speaking"),
    ("writing", "Writing"),
]


def build_student_skill_cards(student, course, build_skill_note_display):
    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related(
            "subskill_assessments",
        )
        .order_by("skill")
    )

    assessments_by_skill = {
        assessment.skill: assessment
        for assessment in skill_assessments
    }

    skills = []

    for skill_value, skill_name in SKILL_AREAS:
        assessment = assessments_by_skill.get(
            skill_value
        )

        expected_subskills = SUBSKILLS.get(
            skill_value,
            [],
        )

        total_subskills_count = len(
            expected_subskills
        )

        existing_subskills = {}

        if assessment:
            existing_subskills = {
                subskill.subskill: subskill
                for subskill
                in assessment.subskill_assessments.all()
            }

        subskills_display = []
        assessed_subskills_count = 0

        for subskill_value, subskill_label in expected_subskills:
            subskill_assessment = (
                existing_subskills.get(
                    subskill_value
                )
            )

            is_assessed = bool(
                subskill_assessment
                and subskill_assessment.rating
            )

            if is_assessed:
                assessed_subskills_count += 1

            subskills_display.append({
                "value": subskill_value,
                "name": subskill_label,
                "assessment": subskill_assessment,
                "is_assessed": is_assessed,
                "rating": (
                    subskill_assessment.get_rating_display()
                    if is_assessed
                    else None
                ),
            })

        if assessment:
            note_display = build_skill_note_display(
                assessment
            )

            score = (
                assessment.average_score
                if assessed_subskills_count > 0
                else None
            )

            skills.append({
                "assessment": assessment,
                "assessment_id": assessment.id,
                "skill_value": skill_value,
                "name": skill_name,
                "icon": SKILL_ICONS.get(
                    skill_value,
                    "fa-solid fa-chart-simple",
                ),
                "score": score,
                "teacher_notes": assessment.teacher_notes,
                "subskills": subskills_display,
                "assessed_subskills_count":
                    assessed_subskills_count,
                "total_subskills_count":
                    total_subskills_count,
                "strengths":
                    note_display["strengths"],
                "confident":
                    note_display["confident"],
                "required_standard":
                    note_display["required_standard"],
                "developing":
                    note_display["developing"],
                "needs_work":
                    note_display["needs_work"],
            })

        else:
            skills.append({
                "assessment": None,
                "assessment_id": None,
                "skill_value": skill_value,
                "name": skill_name,
                "icon": SKILL_ICONS.get(
                    skill_value,
                    "fa-solid fa-chart-simple",
                ),
                "score": None,
                "teacher_notes": "",
                "subskills": subskills_display,
                "assessed_subskills_count": 0,
                "total_subskills_count":
                    total_subskills_count,
                "strengths": [],
                "confident": [],
                "required_standard": [],
                "developing": [],
                "needs_work": [],
            })

    return skill_assessments, skills