"""
Formal Term Assessment Report generation.

Reads submitted assessment snapshots, resolves reviewed custom narratives for
the overall cross-skill overview and each exact skill-rating combination,
builds a concise Development Focus, and can persist the generated report as a
StudentTermAssessmentReport.
"""

import json

from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction

from profiles.models import (
    SUBSKILLS,
    StudentSubSkillAssessment,
    StudentTermAssessment,
    StudentTermAssessmentReport,
)
from .term_assessment_listening_narratives import (
    LISTENING_PERFORMANCE_NARRATIVES,
    LISTENING_SUBSKILL_ORDER,
)
from .term_assessment_overall_summary_narratives import (
    OVERALL_SUMMARY_AREA_LANGUAGE,
    OVERALL_SUMMARY_NARRATIVES,
)
from .term_assessment_reading_narratives import (
    READING_PERFORMANCE_NARRATIVES,
    READING_SUBSKILL_ORDER,
)
from .term_assessment_speaking_narratives import (
    SPEAKING_PERFORMANCE_NARRATIVES,
    SPEAKING_SUBSKILL_ORDER,
)
from .term_assessment_writing_narratives import (
    WRITING_PERFORMANCE_NARRATIVES,
    WRITING_SUBSKILL_ORDER,
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
SKILL_ORDER = tuple(SKILL_LABELS)

PERFORMANCE_NARRATIVE_CONFIG = {
    "speaking": {
        "order": SPEAKING_SUBSKILL_ORDER,
        "narratives": SPEAKING_PERFORMANCE_NARRATIVES,
    },
    "reading": {
        "order": READING_SUBSKILL_ORDER,
        "narratives": READING_PERFORMANCE_NARRATIVES,
    },
    "listening": {
        "order": LISTENING_SUBSKILL_ORDER,
        "narratives": LISTENING_PERFORMANCE_NARRATIVES,
    },
    "writing": {
        "order": WRITING_SUBSKILL_ORDER,
        "narratives": WRITING_PERFORMANCE_NARRATIVES,
    },
}

DEVELOPMENT_FOCUS_AREAS = {
    "speaking": {
        "fluency": "greater fluency in spoken communication",
        "accuracy_and_range": (
            "greater grammatical accuracy and broader language range "
            "in spoken communication"
        ),
        "pronunciation": "clearer pronunciation",
        "interaction": "more confident spoken interaction",
    },
    "reading": {
        "scanning": "more efficient location of specific information when reading",
        "skimming": (
            "more effective identification of main ideas and overall purpose "
            "when reading"
        ),
        "detailed": "stronger detailed comprehension when reading",
    },
    "listening": {
        "gist": "more reliable understanding of the main message when listening",
        "specific_information": (
            "more effective identification of specific information and key "
            "details when listening"
        ),
        "detailed": "stronger detailed comprehension when listening",
    },
    "writing": {
        "organization": "clearer organisation in written work",
        "cohesion": "stronger cohesion in written work",
        "vocabulary_grammar": (
            "greater grammatical accuracy and broader language range "
            "in written work"
        ),
        "register": "more flexible control of tone and style in written work",
    },
}

CONSOLIDATION_FOCUS_AREAS = {
    "speaking": {
        "fluency": "fluency in spoken communication",
        "accuracy_and_range": "grammatical accuracy and language range in speaking",
        "pronunciation": "pronunciation",
        "interaction": "spoken interaction",
    },
    "reading": {
        "scanning": "locating specific information when reading",
        "skimming": "identifying main ideas and overall purpose when reading",
        "detailed": "detailed comprehension when reading",
    },
    "listening": {
        "gist": "understanding the main message when listening",
        "specific_information": (
            "identifying specific information and key details when listening"
        ),
        "detailed": "detailed comprehension when listening",
    },
    "writing": {
        "organization": "organisation and clear presentation in written work",
        "cohesion": "cohesion in written work",
        "vocabulary_grammar": "grammatical accuracy and language range in written work",
        "register": "control of tone and style in written work",
    },
}


# ---------------------------------------------------------
# VALIDATION AND DATA COLLECTION
# ---------------------------------------------------------

def get_report_assessment_data(assessment):
    """Return validated, ordered skill and subskill data from a submitted assessment."""
    if assessment.status != StudentTermAssessment.Status.SUBMITTED:
        raise ValidationError("Only submitted assessments can generate reports.")

    if assessment.overall_score is None:
        raise ValidationError("The assessment has no overall score.")

    snapshots = list(
        assessment.skill_snapshots.prefetch_related("subskill_assessments")
    )
    snapshot_map = {snapshot.skill: snapshot for snapshot in snapshots}

    if len(snapshots) != len(SKILL_ORDER) or set(snapshot_map) != set(SKILL_ORDER):
        raise ValidationError("The assessment must contain all four skills.")

    skills = []
    subskills = []

    for skill in SKILL_ORDER:
        snapshot = snapshot_map[skill]

        if snapshot.score is None:
            raise ValidationError(f"{SKILL_LABELS[skill]} has no calculated score.")

        expected_subskills = dict(SUBSKILLS[skill])
        records = list(snapshot.subskill_assessments.all())
        record_map = {record.subskill: record for record in records}

        if (
            len(records) != len(expected_subskills)
            or set(record_map) != set(expected_subskills)
        ):
            raise ValidationError(
                f"{SKILL_LABELS[skill]} has incomplete subskill records."
            )

        skills.append({
            "key": skill,
            "label": SKILL_LABELS[skill],
            "score": snapshot.score,
        })

        for subskill, label in expected_subskills.items():
            record = record_map[subskill]

            if record.rating not in SCORES:
                raise ValidationError(
                    f"{SKILL_LABELS[skill]}: {label} has an invalid or missing rating."
                )

            subskills.append({
                "skill": skill,
                "subskill": subskill,
                "rating": record.rating,
                "score": SCORES[record.rating],
            })

    return skills, subskills


# ---------------------------------------------------------
# SHARED REPORT HELPERS
# ---------------------------------------------------------

def _rating_value(rating):
    return getattr(rating, "value", rating)


def _join_items(items):
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])} and {items[-1]}"


# ---------------------------------------------------------
# OVERALL PERFORMANCE OVERVIEW
# ---------------------------------------------------------

def _analyse_overall_summary_skill(skill, items):
    """
    Return factual information about one skill's actual subskill ratings.

    No new rating or pseudo-rating is created. The flags only describe what
    is present in the submitted assessment.
    """
    expected_subskills = [key for key, _ in SUBSKILLS[skill]]

    if len(items) != len(expected_subskills):
        raise ValidationError(
            f"Cannot generate a complete {SKILL_LABELS[skill]} overview."
        )

    item_map = {item["subskill"]: item for item in items}

    if set(item_map) != set(expected_subskills):
        raise ValidationError(
            f"{SKILL_LABELS[skill]} overview contains an invalid subskill structure."
        )

    ordered_items = [item_map[subskill] for subskill in expected_subskills]
    ratings = [_rating_value(item["rating"]) for item in ordered_items]

    return {
        "skill": skill,
        "items": ordered_items,
        "average_score": (
            sum(item["score"] for item in ordered_items) / len(ordered_items)
        ),
        "all_strong": all(rating == RATING.STRONG for rating in ratings),
        "all_confident_or_strong": all(
            rating in (RATING.CONFIDENT, RATING.STRONG)
            for rating in ratings
        ),
        "all_satisfactory_or_above": all(
            rating in (
                RATING.SATISFACTORY,
                RATING.CONFIDENT,
                RATING.STRONG,
            )
            for rating in ratings
        ),
        "developing": [
            item for item in ordered_items
            if _rating_value(item["rating"]) == RATING.DEVELOPING
        ],
        "needs_work": [
            item for item in ordered_items
            if _rating_value(item["rating"]) == RATING.NEEDS_WORK
        ],
        "at_or_above_standard": [
            item for item in ordered_items
            if _rating_value(item["rating"]) in (
                RATING.SATISFACTORY,
                RATING.CONFIDENT,
                RATING.STRONG,
            )
        ],
    }


def _overall_skill_subject(skills, learner_name=None):
    """Return a natural plural subject for one or more language skills."""
    labels = [SKILL_LABELS[skill].lower() for skill in skills]

    if learner_name:
        if len(labels) == 1:
            return f"{learner_name}'s {labels[0]} skills"
        return f"{learner_name}'s skills in {_join_items(labels)}"

    if len(labels) == 1:
        return f"{labels[0]} skills"

    return f"{_join_items(labels)} skills"


def _summary_area_details(skill, items):
    details = []

    for item in items:
        try:
            details.append(
                OVERALL_SUMMARY_AREA_LANGUAGE[skill][item["subskill"]]
            )
        except KeyError as exc:
            raise ValidationError(
                "No overall-summary wording exists for "
                f"{skill}: {item['subskill']}."
            ) from exc

    return details


def _summary_area_text(skill, items):
    return _join_items([
        detail["label"]
        for detail in _summary_area_details(skill, items)
    ])


def _summary_area_verb(skill, items, singular, plural):
    details = _summary_area_details(skill, items)

    if len(details) == 1 and not details[0]["plural"]:
        return singular

    return plural


def _sort_summary_skills(skills, analyses, reverse=True):
    """
    Order skills by their actual assessed results, never by skill identity.

    Existing assessment order is retained only where averages tie.
    """
    position = {skill: index for index, skill in enumerate(SKILL_ORDER)}

    return sorted(
        skills,
        key=lambda skill: (
            analyses[skill]["average_score"],
            -position[skill],
        ),
        reverse=reverse,
    )


def _build_positive_overview_sentence(analyses, learner_name):
    strong = []
    established = []
    satisfactory = []

    for skill, facts in analyses.items():
        if facts["all_strong"]:
            strong.append(skill)
        elif facts["all_confident_or_strong"]:
            established.append(skill)
        elif facts["all_satisfactory_or_above"]:
            satisfactory.append(skill)

    strong = _sort_summary_skills(strong, analyses)
    established = _sort_summary_skills(established, analyses)
    satisfactory = _sort_summary_skills(satisfactory, analyses)

    positive_count = len(strong) + len(established) + len(satisfactory)

    if positive_count == 4 and len(strong) == 4:
        return OVERALL_SUMMARY_NARRATIVES["all_strong"].format(
            learner_name=learner_name
        )

    if positive_count == 4 and len(established) == 4:
        return OVERALL_SUMMARY_NARRATIVES["all_established"].format(
            learner_name=learner_name
        )

    if positive_count == 4 and len(satisfactory) == 4:
        return OVERALL_SUMMARY_NARRATIVES["all_satisfactory"].format(
            learner_name=learner_name
        )

    present = [
        name
        for name, group in (
            ("strong", strong),
            ("established", established),
            ("satisfactory", satisfactory),
        )
        if group
    ]

    if not present:
        return None

    key = f"positive_{'_'.join(present)}"
    first_group = present[0]
    context = {}

    if strong:
        context["strong_subject"] = _overall_skill_subject(
            strong,
            learner_name if first_group == "strong" else None,
        )

    if established:
        context["established_subject"] = _overall_skill_subject(
            established,
            learner_name if first_group == "established" else None,
        )

    if satisfactory:
        context["satisfactory_subject"] = _overall_skill_subject(
            satisfactory,
            learner_name if first_group == "satisfactory" else None,
        )

    try:
        template = OVERALL_SUMMARY_NARRATIVES[key]
    except KeyError as exc:
        raise ValidationError(
            f"No overall-summary narrative exists for pattern: {key}."
        ) from exc

    return template.format(**context)


def _build_one_issue_sentence(skill, facts):
    """Return the custom contrast sentence for one lower-performing skill."""
    developing = facts["developing"]
    needs_work = facts["needs_work"]
    has_standard_or_above = bool(facts["at_or_above_standard"])

    context = {"skill": SKILL_LABELS[skill].lower()}

    if developing:
        context.update({
            "developing_areas": _summary_area_text(skill, developing),
            "developing_verb": _summary_area_verb(
                skill,
                developing,
                "is",
                "are",
            ),
        })

    if needs_work:
        context["needs_work_areas"] = _summary_area_text(skill, needs_work)

    if len(needs_work) == len(facts["items"]):
        key = "one_all_needs_work"
    elif needs_work and developing and has_standard_or_above:
        key = "one_uneven_needs_work_and_developing"
    elif needs_work and has_standard_or_above:
        key = "one_uneven_needs_work"
    elif needs_work and developing:
        key = "one_below_standard_mixed"
    elif len(developing) == len(facts["items"]):
        key = "one_all_developing"
    elif developing:
        key = "one_uneven_developing"
    else:
        raise ValidationError(
            f"{SKILL_LABELS[skill]} does not contain an overview development issue."
        )

    try:
        template = OVERALL_SUMMARY_NARRATIVES[key]
    except KeyError as exc:
        raise ValidationError(
            f"No overall-summary narrative exists for pattern: {key}."
        ) from exc

    return template.format(**context)


def _build_multiple_issue_sentence(issue_skills, analyses):
    """Return one concise contrast sentence covering two or three skills."""
    has_needs_work = any(
        analyses[skill]["needs_work"]
        for skill in issue_skills
    )
    has_developing = any(
        analyses[skill]["developing"]
        for skill in issue_skills
    )
    skills = _join_items([
        SKILL_LABELS[skill].lower()
        for skill in issue_skills
    ])

    if has_needs_work and has_developing:
        key = "multiple_needs_work_and_developing"
    elif has_needs_work:
        key = "multiple_needs_work"
    else:
        key = "multiple_developing"

    return OVERALL_SUMMARY_NARRATIVES[key].format(skills=skills)


def _build_all_four_issue_sentence(analyses, learner_name):
    """Return one overview when every skill contains lower-rated areas."""
    has_needs_work = any(
        facts["needs_work"]
        for facts in analyses.values()
    )
    has_developing = any(
        facts["developing"]
        for facts in analyses.values()
    )

    if has_needs_work and has_developing:
        key = "all_four_needs_work_and_developing"
    elif has_needs_work:
        key = "all_four_needs_work"
    else:
        key = "all_four_developing"

    return OVERALL_SUMMARY_NARRATIVES[key].format(
        learner_name=learner_name
    )


def build_overall_performance_summary(subskills, learner_name):
    """
    Build the short cross-skill overview shown before the four detailed
    Performance Summary paragraphs.

    The rhetorical order is driven by the actual assessment pattern:
    established/stronger skills first, followed by a concise contrast where
    development is needed. No fixed skill order, strongest/weakest labels or
    numerical-to-verbal overall rating is used.
    """
    analyses = {}

    for skill in SKILL_ORDER:
        items = [
            item
            for item in subskills
            if item["skill"] == skill
        ]
        analyses[skill] = _analyse_overall_summary_skill(skill, items)

    positive_sentence = _build_positive_overview_sentence(
        analyses,
        learner_name,
    )

    issue_skills = [
        skill
        for skill, facts in analyses.items()
        if facts["developing"] or facts["needs_work"]
    ]

    issue_skills = sorted(
        issue_skills,
        key=lambda skill: (
            min(item["score"] for item in analyses[skill]["items"]),
            analyses[skill]["average_score"],
        ),
    )

    if not issue_skills:
        if positive_sentence is None:
            raise ValidationError(
                "Unable to determine an overall Performance Summary overview."
            )
        return positive_sentence

    if not positive_sentence:
        return _build_all_four_issue_sentence(
            analyses,
            learner_name,
        )

    if len(issue_skills) == 1:
        contrast_sentence = _build_one_issue_sentence(
            issue_skills[0],
            analyses[issue_skills[0]],
        )
    else:
        contrast_sentence = _build_multiple_issue_sentence(
            issue_skills,
            analyses,
        )

    return f"{positive_sentence} {contrast_sentence}"


# ---------------------------------------------------------
# DETAILED PERFORMANCE SUMMARY
# ---------------------------------------------------------

def build_skill_performance_summary(skill, items, learner_name):
    """Return the reviewed custom narrative for one exact skill-rating combination."""
    try:
        config = PERFORMANCE_NARRATIVE_CONFIG[skill]
    except KeyError as exc:
        raise ValidationError(f"Unsupported report skill: {skill}.") from exc

    expected_order = tuple(config["order"])

    if len(items) != len(expected_order):
        raise ValidationError(
            f"{SKILL_LABELS[skill]} performance requires exactly "
            f"{len(expected_order)} subskill ratings."
        )

    ratings = {}

    for item in items:
        subskill = item["subskill"]

        if subskill not in expected_order:
            raise ValidationError(
                f"Unsupported {SKILL_LABELS[skill]} subskill: {subskill}."
            )

        if subskill in ratings:
            raise ValidationError(
                f"Duplicate {SKILL_LABELS[skill]} subskill: {subskill}."
            )

        rating = _rating_value(item["rating"])

        if rating not in RATING.values:
            raise ValidationError(
                f"Unsupported {SKILL_LABELS[skill]} rating: {rating}."
            )

        ratings[subskill] = rating

    if set(ratings) != set(expected_order):
        raise ValidationError(
            f"{SKILL_LABELS[skill]} performance contains "
            "an invalid subskill structure."
        )

    combination = tuple(
        ratings[subskill]
        for subskill in expected_order
    )

    try:
        narrative = config["narratives"][combination]
    except KeyError as exc:
        raise ValidationError(
            f"No {SKILL_LABELS[skill]} performance narrative "
            f"exists for ratings: {combination}."
        ) from exc

    return narrative.format(learner_name=learner_name)


def build_performance_summary(subskills, learner_name):
    """
    Return exactly four detailed Performance Summary paragraphs.

    Each paragraph comes directly from the reviewed custom narrative
    dictionary for that skill.
    """
    paragraphs = []

    for skill in SKILL_ORDER:
        items = [
            item for item in subskills
            if item["skill"] == skill
        ]

        paragraphs.append(
            build_skill_performance_summary(
                skill,
                items,
                learner_name,
            )
        )

    return paragraphs


# ---------------------------------------------------------
# DEVELOPMENT FOCUS
# ---------------------------------------------------------

def _focus_area(mapping, item):
    try:
        return mapping[item["skill"]][item["subskill"]]
    except KeyError as exc:
        raise ValidationError(
            "No Development Focus wording exists for "
            f"{item['skill']}: {item['subskill']}."
        ) from exc


def build_development_focus(subskills):
    """
    Return one concise Development Focus paragraph.

    Needs Work and Developing areas take priority. If none exist,
    Satisfactory areas are selected for consolidation. If every assessed
    subskill is Confident or Strong, use one general extension statement.
    """
    development = sorted(
        (
            item
            for item in subskills
            if _rating_value(item["rating"]) in (
                RATING.NEEDS_WORK,
                RATING.DEVELOPING,
            )
        ),
        key=lambda item: item["score"],
    )

    if development:
        areas = _join_items([
            _focus_area(DEVELOPMENT_FOCUS_AREAS, item)
            for item in development[:MAX_PRIORITIES]
        ])

        return (
            "The next learning period should prioritise "
            f"{areas}."
        )

    satisfactory = [
        item
        for item in subskills
        if _rating_value(item["rating"]) == RATING.SATISFACTORY
    ]

    if satisfactory:
        areas = _join_items([
            _focus_area(CONSOLIDATION_FOCUS_AREAS, item)
            for item in satisfactory[:MAX_PRIORITIES]
        ])

        return (
            "The next learning period should focus on consolidating "
            f"{areas}."
        )

    return (
        "The next learning period should focus on consolidating and extending "
        "established performance across all four language skills."
    )


# ---------------------------------------------------------
# COMPLETE REPORT GENERATION
# ---------------------------------------------------------

def generate_term_assessment_report(assessment):
    """
    Assemble the stored report content from a submitted Formal Term Assessment.

    Returns report data only. Does not save or overwrite a report.
    """
    skills, subskills = get_report_assessment_data(assessment)

    student = assessment.enrollment.student
    learner_name = student.first_name.strip() or student.username

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
        "performance_summary_overview": build_overall_performance_summary(
            subskills,
            learner_name,
        ),
        "performance_summary_paragraphs": build_performance_summary(
            subskills,
            learner_name,
        ),
        "development_focus": build_development_focus(subskills),
    }


# ---------------------------------------------------------
# PERSISTENT REPORT CREATION
# ---------------------------------------------------------

@transaction.atomic
def create_term_assessment_report(assessment, generated_by):
    """
    Generate and persist one report for a submitted assessment.

    Existing reports are never regenerated or overwritten.
    """
    if generated_by is None or not generated_by.pk:
        raise ValidationError("A report must have a valid generating user.")

    assessment = (
        StudentTermAssessment.objects
        .select_for_update()
        .get(pk=assessment.pk)
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

    report_data = generate_term_assessment_report(assessment)

    report_content = json.loads(
        json.dumps(
            report_data,
            cls=DjangoJSONEncoder,
        )
    )

    return StudentTermAssessmentReport.objects.create(
        assessment=assessment,
        content=report_content,
        generated_by=generated_by,
    )
