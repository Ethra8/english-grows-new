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

from .term_assessment_listening_narratives import (
    LISTENING_PERFORMANCE_NARRATIVES,
    LISTENING_SUBSKILL_ORDER,
)

from profiles.utils.term_assessment_writing_narratives import (
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

SUBSKILL_LABELS = {
    skill: dict(subskills)
    for skill, subskills in SUBSKILLS.items()
}

REPORT_SUMMARY_AREAS = {
    "speaking": {
        "fluency": "fluency",
        "accuracy_and_range": "grammatical accuracy and language range",
        "pronunciation": "pronunciation",
        "interaction": "interaction",
    },
    "reading": {
        "scanning": "locating specific information",
        "skimming": "identifying main ideas and overall purpose",
        "detailed": "understanding detailed information",
    },
    "listening": {
        "gist": "understanding the main idea and overall message",
        "specific_information": "identifying specific information",
        "detailed": "understanding detailed meaning",
    },
    "writing": {
        "organization": "the organisation and clear presentation of written work",
        "cohesion": "cohesion",
        "vocabulary_grammar": "grammatical accuracy and language range",
        "register": "control of register",
    },
}

DEVELOPMENT_FOCUS_AREAS = {
    "speaking": {
        "fluency": "greater fluency",
        "accuracy_and_range": "greater grammatical accuracy and broader language range",
        "pronunciation": "clearer pronunciation",
        "interaction": "more confident interaction",
    },
    "reading": {
        "scanning": "more efficient location of specific information",
        "skimming": "more effective identification of main ideas and overall purpose",
        "detailed": "stronger detailed comprehension",
    },
    "listening": {
        "gist": "more reliable understanding of the main message",
        "specific_information": "more effective identification of specific information",
        "detailed": "stronger detailed comprehension",
    },
    "writing": {
        "organization": "clearer organisation",
        "cohesion": "stronger cohesion",
        "vocabulary_grammar": "greater grammatical accuracy and language range",
        "register": "more flexible control of register",
    },
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



def build_listening_performance_summary(items, learner_name):
    """
    Return the canonical narrative for one exact Listening rating combination.

    Tuple order:
    gist, specific_information, detailed.
    """
    expected_subskills = set(LISTENING_SUBSKILL_ORDER)

    if len(items) != len(expected_subskills):
        raise ValidationError(
            "Listening performance requires exactly three subskill ratings."
        )

    ratings = {}

    for item in items:
        subskill = item["subskill"]
        rating = item["rating"]

        if subskill not in expected_subskills:
            raise ValidationError(
                f"Unsupported Listening subskill: {subskill}."
            )

        if subskill in ratings:
            raise ValidationError(
                f"Duplicate Listening subskill: {subskill}."
            )

        rating_value = getattr(
            rating,
            "value",
            rating,
        )

        if rating_value not in RATING.values:
            raise ValidationError(
                f"Unsupported Listening rating: {rating_value}."
            )

        ratings[subskill] = rating_value

    if set(ratings) != expected_subskills:
        raise ValidationError(
            "Listening performance contains an invalid subskill structure."
        )

    combination = tuple(
        ratings[subskill]
        for subskill in LISTENING_SUBSKILL_ORDER
    )

    try:
        narrative = LISTENING_PERFORMANCE_NARRATIVES[combination]
    except KeyError as exc:
        raise ValidationError(
            f"No Listening performance narrative exists for ratings: {combination}."
        ) from exc

    return narrative.format(
        learner_name=learner_name
    )



def build_writing_performance_summary(items, learner_name):
    """Return the canonical Writing narrative for the exact rating combination."""
    expected_subskills = set(WRITING_SUBSKILL_ORDER)

    if len(items) != len(expected_subskills):
        raise ValidationError(
            "Writing performance requires exactly four subskill ratings."
        )

    ratings = {}

    for item in items:
        subskill = item["subskill"]
        rating = item["rating"]

        if subskill not in expected_subskills:
            raise ValidationError(
                f"Unsupported Writing subskill: {subskill}."
            )

        if subskill in ratings:
            raise ValidationError(
                f"Duplicate Writing subskill: {subskill}."
            )

        rating_value = getattr(rating, "value", rating)

        if rating_value not in RATING.values:
            raise ValidationError(
                f"Unsupported Writing rating: {rating_value}."
            )

        ratings[subskill] = rating_value

    if set(ratings) != expected_subskills:
        raise ValidationError(
            "Writing performance contains an invalid subskill structure."
        )

    combination = tuple(
        ratings[subskill]
        for subskill in WRITING_SUBSKILL_ORDER
    )

    try:
        narrative = WRITING_PERFORMANCE_NARRATIVES[combination]
    except KeyError as exc:
        raise ValidationError(
            f"No Writing performance narrative exists for ratings: {combination}."
        ) from exc

    return narrative.format(learner_name=learner_name)


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

    if skill == "listening":
        return build_listening_performance_summary(
            items,
            learner_name,
        )
    
    if skill == "writing":
        return build_writing_performance_summary(
            items,
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
# INTEGRATED PERFORMANCE SUMMARY
# ---------------------------------------------------------

def _join_report_areas(items):
    """Join concise report areas without awkward repeated 'and'."""
    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        if " and " in items[0] or " and " in items[1]:
            return f"{items[0]}, or {items[1]}"
        return f"{items[0]} and {items[1]}"

    return f"{', '.join(items[:-1])} and {items[-1]}"


def _sentence_case(text):
    """Capitalise the first character of a generated clause."""
    return text[:1].upper() + text[1:]


def _overall_performance_language(score):
    if score < 4.5:
        return "requires substantial further development"

    if score < 5.5:
        return "is still developing"

    if score < 6.75:
        return "is satisfactory"

    if score < 8.75:
        return "is generally confident"

    return "is strong"


# def _build_integrated_rating_clause(rating, areas):
#     """Return one concise descriptive clause for a rating group."""
#     area_text = _join_report_areas(areas)

#     if rating == RATING.STRONG:
#         return f"clear strengths are evident in {area_text}"

#     if rating == RATING.CONFIDENT:
#         return f"confidence is evident in {area_text}"

#     if rating == RATING.SATISFACTORY:
#         return f"performance meets the expected standard in {area_text}"

#     if rating == RATING.DEVELOPING:
#         return f"{area_text} is still developing"

#     if rating == RATING.NEEDS_WORK:
#         return f"greater support is required in {area_text}"

#     raise ValidationError(
#         "Invalid rating in integrated performance summary."
#     )


# def _build_integrated_skill_summary(skill, items, include_skill=True):
#     """Return a concise one- or two-sentence interpretation of one skill."""
#     rating_order = (
#         RATING.STRONG,
#         RATING.CONFIDENT,
#         RATING.SATISFACTORY,
#         RATING.DEVELOPING,
#         RATING.NEEDS_WORK,
#     )

#     groups = {rating: [] for rating in rating_order}

#     for item in items:
#         groups[item["rating"]].append(
#             REPORT_SUMMARY_AREAS[skill][item["subskill"]]
#         )

#     clauses = [
#         _build_integrated_rating_clause(rating, groups[rating])
#         for rating in rating_order
#         if groups[rating]
#     ]

#     sentences = []

#     for index in range(0, len(clauses), 2):
#         pair = clauses[index:index + 2]

#         if index == 0 and include_skill:
#             sentence = (
#                 f"In {SKILL_LABELS[skill].lower()}, {pair[0]}"
#             )
#         else:
#             sentence = _sentence_case(pair[0])

#         if len(pair) == 2:
#             sentence += f". However, {pair[1]}"

#         sentences.append(f"{sentence}.")

#     return " ".join(sentences)


def build_integrated_performance_summary(
    skills,
    subskills,
    learner_name,
):
    """
    Build the report Performance Summary as four paragraphs,
    one for each assessed skill.

    Each paragraph uses the reviewed canonical narrative for the exact
    subskill-rating combination.

    Skills are ordered from highest to lowest score. The first paragraph
    also provides the overall assessment context. Ties are handled without
    inventing differences between equally scored skills.
    """
    skill_map = {
        item["key"]: item
        for item in skills
    }

    if set(skill_map) != set(SKILL_LABELS):
        raise ValidationError(
            "Integrated performance summary requires all four skills."
        )

    # These are the reviewed 625 / 125 / 125 / 625 canonical narratives.
    skill_summaries = build_performance_summary(
        subskills,
        learner_name,
    )

    skill_order = {
        skill: index
        for index, skill in enumerate(SKILL_LABELS)
    }

    ranked_skills = sorted(
        SKILL_LABELS,
        key=lambda skill: (
            -skill_map[skill]["score"],
            skill_order[skill],
        ),
    )

    scores = [
        skill_map[skill]["score"]
        for skill in SKILL_LABELS
    ]

    overall_score = sum(scores) / len(scores)
    highest_score = max(scores)
    lowest_score = min(scores)

    strongest = [
        skill for skill in SKILL_LABELS
        if skill_map[skill]["score"] == highest_score
    ]

    weakest = [
        skill for skill in SKILL_LABELS
        if skill_map[skill]["score"] == lowest_score
    ]

    possessive = (
        f"{learner_name}'"
        if learner_name.lower().endswith("s")
        else f"{learner_name}'s"
    )

    opening = (
        f"{possessive} overall performance "
        f"{_overall_performance_language(overall_score)}"
    )

    if len(strongest) == 1 and highest_score != lowest_score:
        opening += (
            f", with {SKILL_LABELS[strongest[0]].lower()} currently "
            "the strongest of the four assessed skills."
        )
    elif len(strongest) < len(SKILL_LABELS):
        strongest_labels = _join_report_areas([
            SKILL_LABELS[skill].lower()
            for skill in strongest
        ])
        opening += (
            f", with {strongest_labels} currently the strongest "
            "of the assessed skills."
        )
    else:
        opening += (
            ", with broadly consistent performance across "
            "the four assessed skills."
        )

    paragraphs = []

    for index, skill in enumerate(ranked_skills):
        canonical_summary = skill_summaries[skill]

        if index == 0:
            paragraph = (
                f"{opening} "
                f"{canonical_summary}"
            )

        elif (
            len(weakest) == 1
            and skill == weakest[0]
            and highest_score != lowest_score
        ):
            paragraph = (
                f"{SKILL_LABELS[skill]} is currently the least established "
                f"of the four assessed skills. {canonical_summary}"
            )

        else:
            paragraph = (
                f"In {SKILL_LABELS[skill].lower()}, "
                f"{canonical_summary}"
            )

        paragraphs.append(paragraph)

    return paragraphs



# ---------------------------------------------------------
# DEVELOPMENT FOCUS
# ---------------------------------------------------------

def _build_skill_development_clause(
    skill,
    items,
    include_consolidation=False,
):
    """Return a concise development direction for one language skill."""
    development_items = [
        item for item in items
        if item["rating"] in (
            RATING.NEEDS_WORK,
            RATING.DEVELOPING,
        )
    ]

    development_items = sorted(
        development_items,
        key=lambda item: item["score"],
    )[:2]

    if development_items:
        areas = _join_report_areas([
            DEVELOPMENT_FOCUS_AREAS[skill][item["subskill"]]
            for item in development_items
        ])

        if skill == "speaking":
            clause = (
                f"prioritise {areas} in spoken communication"
            )
        elif skill == "writing":
            clause = f"focus particularly on {areas}"
        else:
            clause = f"focus on {areas}"

        if include_consolidation:
            consolidation_items = [
                item for item in items
                if item["rating"] in (
                    RATING.SATISFACTORY,
                    RATING.CONFIDENT,
                    RATING.STRONG,
                )
            ][:2]

            if consolidation_items:
                consolidation = _join_report_areas([
                    REPORT_SUMMARY_AREAS[skill][item["subskill"]]
                    for item in consolidation_items
                ])
                clause += (
                    f", while continuing to consolidate {consolidation}"
                )

        return clause

    satisfactory_items = [
        item for item in items
        if item["rating"] == RATING.SATISFACTORY
    ][:2]

    if satisfactory_items:
        areas = _join_report_areas([
            REPORT_SUMMARY_AREAS[skill][item["subskill"]]
            for item in satisfactory_items
        ])
        return f"continue to consolidate {areas}"

    return "continue to consolidate and extend established performance"


def build_development_focus(subskills):
    """
    Build one concise Development Focus paragraph across all four skills.

    Up to two Needs Work / Developing areas are selected within each skill.
    Where one skill has the uniquely strongest overall profile, established
    areas within that skill may also be acknowledged for consolidation.
    """
    items_by_skill = {}

    for skill in SKILL_LABELS:
        items = [
            item for item in subskills
            if item["skill"] == skill
        ]

        if len(items) != len(SUBSKILLS[skill]):
            raise ValidationError(
                f"Cannot generate complete {SKILL_LABELS[skill]} development focus."
            )

        items_by_skill[skill] = items

    skill_averages = {
        skill: (
            sum(item["score"] for item in items)
            / len(items)
        )
        for skill, items in items_by_skill.items()
    }

    highest_score = max(skill_averages.values())
    strongest = [
        skill for skill, score in skill_averages.items()
        if score == highest_score
    ]
    unique_strongest = (
        strongest[0]
        if len(strongest) == 1
        else None
    )

    clauses = {
        skill: _build_skill_development_clause(
            skill,
            items_by_skill[skill],
            include_consolidation=(skill == unique_strongest),
        )
        for skill in SKILL_LABELS
    }

    return (
        f"The next learning period should {clauses['speaking']}. "
        f"Reading should {clauses['reading']}, while listening should "
        f"{clauses['listening']}. "
        f"Written work should {clauses['writing']}."
    )


# ---------------------------------------------------------
# SKILL-SPECIFIC DEVELOPMENT PRIORITIES
# ---------------------------------------------------------
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
        # New concise report structure
        "performance_summary_paragraphs": build_integrated_performance_summary(
            skills,
            subskills,
            learner_name,
        ),
        "development_focus": build_development_focus(subskills),

        # Existing fields kept temporarily
        "performance_summary": build_performance_summary(
            subskills,
            learner_name,
        ),
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