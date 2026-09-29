"""
Rule-based generation of Formal Term Assessment Reports.

Reads submitted assessment data and assembles a structured report.
Does not modify assessments, save reports or publish results.
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

from .term_assessment_speaking_narratives import (
    SPEAKING_PERFORMANCE_NARRATIVES,
    SPEAKING_SUBSKILL_ORDER,
)

from .term_assessment_reading_narratives import (
    READING_PERFORMANCE_NARRATIVES,
    READING_SUBSKILL_ORDER,
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
# SKILLS PERFORMANCE PROFILE
# ---------------------------------------------------------

SPEAKING_RATING_LEVELS = {
    RATING.NEEDS_WORK: 1,
    RATING.DEVELOPING: 2,
    RATING.SATISFACTORY: 3,
    RATING.CONFIDENT: 4,
    RATING.STRONG: 5,
}

READING_RATING_LEVELS = {
    RATING.NEEDS_WORK: 1,
    RATING.DEVELOPING: 2,
    RATING.SATISFACTORY: 3,
    RATING.CONFIDENT: 4,
    RATING.STRONG: 5,
}


def analyse_speaking_profile(items):
    """
    Analyse the relationship between the four Speaking ratings.

    The ordinal levels are used only to identify the shape of the
    performance profile. They do not replace or modify assessment scores.
    """
    ratings = {
        item["subskill"]: item["rating"]
        for item in items
    }

    expected = {
        "fluency",
        "accuracy_and_range",
        "pronunciation",
        "interaction",
    }

    if set(ratings) != expected:
        raise ValidationError(
            "Cannot analyse an incomplete Speaking assessment."
        )

    levels = {
        subskill: SPEAKING_RATING_LEVELS[rating]
        for subskill, rating in ratings.items()
    }

    lowest = min(levels.values())
    highest = max(levels.values())
    spread = highest - lowest

    # -----------------------------------------------------
    # UNEVEN PROFILE
    # -----------------------------------------------------
    if spread >= 2:
        highest_items = [
            subskill
            for subskill, level in levels.items()
            if level == highest
        ]
        lowest_items = [
            subskill
            for subskill, level in levels.items()
            if level == lowest
        ]

        # One clear strength against three closely grouped areas.
        if (
            len(highest_items) == 1
            and max(
                level
                for subskill, level in levels.items()
                if subskill != highest_items[0]
            ) - min(
                level
                for subskill, level in levels.items()
                if subskill != highest_items[0]
            ) <= 1
        ):
            profile = "pronounced_strength"

        # One clear weakness against three closely grouped areas.
        elif (
            len(lowest_items) == 1
            and max(
                level
                for subskill, level in levels.items()
                if subskill != lowest_items[0]
            ) - min(
                level
                for subskill, level in levels.items()
                if subskill != lowest_items[0]
            ) <= 1
        ):
            profile = "pronounced_weakness"

        else:
            profile = "mixed"

    # -----------------------------------------------------
    # RELATIVELY EVEN PROFILE
    # -----------------------------------------------------
    else:
        average = sum(levels.values()) / len(levels)

        if average >= 4:
            profile = "consistently_strong"
        elif average >= 3:
            profile = "generally_secure"
        elif average >= 2:
            profile = "developing_evenly"
        else:
            profile = "broad_support_needed"

    stronger = [
        subskill
        for subskill, level in levels.items()
        if level == highest
    ]

    weaker = [
        subskill
        for subskill, level in levels.items()
        if level == lowest
    ]

    middle = [
        subskill
        for subskill, level in levels.items()
        if lowest < level < highest
    ]

    return {
        "profile": profile,
        "ratings": ratings,
        "levels": levels,
        "stronger": stronger,
        "middle": middle,
        "weaker": weaker,
    }



def analyse_reading_profile(items):
    """
    Analyse the relationship between the three Reading subskill ratings.

    The returned profile describes the shape of performance independently
    from the absolute rating level. Narrative generation is handled
    separately.
    """
    expected_subskills = [
        subskill
        for subskill, _ in SUBSKILLS["reading"]
    ]

    if len(items) != len(expected_subskills):
        raise ValidationError(
            "Reading assessment must contain all three subskills."
        )

    raw_ratings = {}

    for item in items:
        subskill = item.get("subskill")
        rating = item.get("rating")

        if subskill not in expected_subskills:
            raise ValidationError(
                "Reading assessment contains an invalid subskill."
            )

        if subskill in raw_ratings:
            raise ValidationError(
                "Reading assessment contains a duplicate subskill."
            )

        if rating not in READING_RATING_LEVELS:
            raise ValidationError(
                "Reading assessment contains an invalid rating."
            )

        raw_ratings[subskill] = rating

    if set(raw_ratings) != set(expected_subskills):
        raise ValidationError(
            "Reading assessment must contain all three subskills."
        )

    ratings = {
        subskill: raw_ratings[subskill]
        for subskill in expected_subskills
    }
    levels = {
        subskill: READING_RATING_LEVELS[rating]
        for subskill, rating in ratings.items()
    }

    lowest = min(levels.values())
    highest = max(levels.values())
    spread = highest - lowest

    stronger = [
        subskill
        for subskill, level in levels.items()
        if level == highest
    ]
    weaker = [
        subskill
        for subskill, level in levels.items()
        if level == lowest
    ]
    middle = [
        subskill
        for subskill, level in levels.items()
        if lowest < level < highest
    ]

    if spread >= 2:
        ordered_levels = sorted(levels.values())
        lower_gap = ordered_levels[1] - ordered_levels[0]
        upper_gap = ordered_levels[2] - ordered_levels[1]

        if upper_gap > lower_gap:
            profile_name = "pronounced_strength"
        elif lower_gap > upper_gap:
            profile_name = "pronounced_weakness"
        else:
            profile_name = "mixed"
    else:
        average = sum(levels.values()) / len(levels)

        if average >= 4:
            profile_name = "consistently_strong"
        elif average >= 3:
            profile_name = "generally_secure"
        elif average >= 2:
            profile_name = "developing_evenly"
        else:
            profile_name = "broad_support_needed"

    return {
        "profile": profile_name,
        "ratings": ratings,
        "levels": levels,
        "stronger": stronger,
        "middle": middle,
        "weaker": weaker,
    }



def get_stronger_area_language(level, plural=False):
    if level == 5:
        return "clear strengths" if plural else "a particular strength"
    if level == 4:
        return "more confident areas" if plural else "a more confident area"
    return "more established areas" if plural else "a more established area"


def get_weaker_area_language(level, plural=False):
    if level == 1:
        return "least established areas" if plural else "the least established area"
    if level == 2:
        return "less consistent areas" if plural else "a less consistent area"
    return "comparatively less secure areas" if plural else "a comparatively less secure area"



def build_speaking_performance_summary(profile, learner_name):
    """
    Return the canonical narrative for one exact Speaking rating combination.

    Tuple order:
    fluency, accuracy_and_range, pronunciation, interaction.
    """
    combination = tuple(
        getattr(
            profile["ratings"][subskill],
            "value",
            profile["ratings"][subskill],
        )
        for subskill in SPEAKING_SUBSKILL_ORDER
    )

    try:
        narrative = SPEAKING_PERFORMANCE_NARRATIVES[combination]
    except KeyError as exc:
        raise ValidationError(
            f"No Speaking performance narrative exists for ratings: {combination}."
        ) from exc

    return narrative.format(
        learner_name=learner_name
    )


def get_reading_status_language(level, plural=False):
    if level == 5:
        return "are clear strengths" if plural else "is a clear strength"
    if level == 4:
        return "are confident areas" if plural else "is a confident area"
    if level == 3:
        return "are satisfactory for this level" if plural else "is satisfactory for this level"
    if level == 2:
        return "are still developing" if plural else "is still developing"
    return "remain less established" if plural else "remains less established"


def build_reading_performance_summary(profile, learner_name):
    """
    Return the canonical narrative for one exact Reading rating combination.

    Tuple order:
    scanning, skimming, detailed.
    """
    combination = tuple(
        getattr(
            profile["ratings"][subskill],
            "value",
            profile["ratings"][subskill],
        )
        for subskill in READING_SUBSKILL_ORDER
    )

    try:
        narrative = READING_PERFORMANCE_NARRATIVES[combination]
    except KeyError as exc:
        raise ValidationError(
            f"No Reading performance narrative exists for ratings: {combination}."
        ) from exc

    return narrative.format(
        learner_name=learner_name
    )



# ---------------------------------------------------------
# PERFORMANCE SUMMARY
# ---------------------------------------------------------

def join_narrative_items(items):
    """Join short report expressions using natural English punctuation."""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])} and {items[-1]}"


def build_performance_rating_sentence(rating, expressions, learner_name):
    """
    Build natural descriptive prose for subskills sharing one rating.

    Performance Summary describes demonstrated performance only.
    It does not provide recommendations or suggest future practice.
    """
    first = expressions[0]
    remaining = expressions[1:]

    if rating == RATING.STRONG:
        if not remaining:
            return f"{learner_name} demonstrates strong ability in {first}."
        return (
            f"{learner_name} demonstrates strong ability in {first}, "
            f"with similarly strong performance in "
            f"{join_narrative_items(remaining)}."
        )

    if rating == RATING.CONFIDENT:
        if not remaining:
            return f"{learner_name} demonstrates confidence in {first}."
        return (
            f"{learner_name} demonstrates confidence in {first}, "
            f"as well as in {join_narrative_items(remaining)}."
        )

    if rating == RATING.SATISFACTORY:
        if not remaining:
            return (
                f"{learner_name} demonstrates satisfactory performance "
                f"in {first}."
            )
        return (
            f"{learner_name} demonstrates satisfactory performance in {first}, "
            f"with a similar level of performance in "
            f"{join_narrative_items(remaining)}."
        )

    if rating == RATING.DEVELOPING:
        if not remaining:
            return (
                f"{learner_name} demonstrates developing performance "
                f"in {first}."
            )
        return (
            f"{learner_name} demonstrates developing performance in {first}, "
            f"with a similar level of performance in "
            f"{join_narrative_items(remaining)}."
        )

    if rating == RATING.NEEDS_WORK:
        if not remaining:
            return (
                f"{learner_name} currently experiences difficulty "
                f"with {first}."
            )
        return (
            f"{learner_name} currently experiences difficulty with {first}, "
            f"as well as with {join_narrative_items(remaining)}."
        )

    raise ValidationError("Invalid rating in performance summary.")


def build_skill_performance_summary(skill, items, learner_name):
    """
    Describe the learner's current demonstrated performance within one
    language skill.

    Speaking uses profile-based interpretation of the relationship between
    its four subskill ratings.

    Other skills currently retain rating-grouped narrative generation.

    Development recommendations and suggested practice belong exclusively
    in Development Priorities.
    """
    if skill == "speaking":
        profile = analyse_speaking_profile(items)
        return build_speaking_performance_summary(profile, learner_name)

    if skill == "reading":
        profile = analyse_reading_profile(items)
        return build_reading_performance_summary(
            profile,
            learner_name,
        )
    
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

    for rating in rating_order:
        expressions = groups[rating]

        if expressions:
            sentences.append(
                build_performance_rating_sentence(
                    rating,
                    expressions,
                    learner_name,
                )
            )

    return " ".join(sentences)


def build_performance_summary(subskills, learner_name):
    """
    Generate four skill-specific descriptive performance paragraphs.

    Every assessed subskill contributes to its corresponding paragraph.
    Ratings and numerical scores are not modified.
    Development recommendations are generated separately.
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

    Needs Work / Developing:
    - provide targeted development guidance.

    Satisfactory:
    - if all subskills are Satisfactory, provide the broader skill-level
      consolidation narrative plus the individual subskill recommendations;
    - if mixed with Confident / Strong only, provide recommendations only
      for the Satisfactory subskills;
    - if mixed with Needs Work / Developing, identify the Satisfactory
      areas for consolidation and provide their recommendations.

    Confident / Strong:
    - if all subskills are Confident or Strong, provide the broader
      consolidation and extension narrative.
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

        # Needs Work / Developing:
        # provide targeted development guidance for each weaker subskill.
        for item in needs_work + developing:
            sentences.append(
                SUBSKILL_DEVELOPMENT_NARRATIVES[skill][item["subskill"]]
            )

        if satisfactory:
            all_satisfactory = len(satisfactory) == len(skill_items)
            has_development = bool(needs_work or developing)

            # Every subskill is Satisfactory:
            # provide the broader skill-level consolidation narrative.
            if all_satisfactory:
                sentences.append(
                    SKILL_SATISFACTORY_NARRATIVES[skill]
                )

            # Satisfactory mixed with Needs Work / Developing:
            # identify the satisfactory areas that should also be consolidated.
            elif has_development:
                expressions = [
                    SUBSKILL_NARRATIVES[skill][item["subskill"]]
                    for item in satisfactory
                ]

                sentences.append(
                    "Further consolidation and improvement are encouraged in "
                    f"{join_narrative_items(expressions)}."
                )

            # Satisfactory mixed only with Confident / Strong:
            # do not characterise the whole skill as Satisfactory.
            # The individual recommendations below identify the specific
            # satisfactory areas that can be developed further.

            for item in satisfactory:
                sentences.append(
                    SUBSKILL_RECOMMENDATIONS[skill][item["subskill"]]
                )

        # No Needs Work, Developing or Satisfactory ratings:
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
    4. Confident / Strong, for extension

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