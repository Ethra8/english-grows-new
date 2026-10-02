"""
Custom learner-facing text for the short cross-skill overview at the start of
a Formal Term Assessment Report.

These templates describe patterns in the learner's actual assessment ratings.
They do not create a second rating scale and they do not rank the four skills.
"""

OVERALL_SUMMARY_AREA_LANGUAGE = {
    "speaking": {
        "fluency": {"label": "fluency", "plural": False},
        "accuracy_and_range": {
            "label": "grammatical accuracy and language range",
            "plural": True,
        },
        "pronunciation": {"label": "pronunciation", "plural": False},
        "interaction": {"label": "spoken interaction", "plural": False},
    },
    "reading": {
        "scanning": {"label": "locating specific information", "plural": False},
        "skimming": {
            "label": "identifying main ideas and overall purpose",
            "plural": False,
        },
        "detailed": {
            "label": "understanding detailed information and meaning in context",
            "plural": False,
        },
    },
    "listening": {
        "gist": {
            "label": "understanding the main ideas and overall message",
            "plural": False,
        },
        "specific_information": {
            "label": "identifying specific information and key details",
            "plural": False,
        },
        "detailed": {
            "label": "understanding detailed information and meaning in context",
            "plural": False,
        },
    },
    "writing": {
        "organization": {
            "label": "organisation and clear presentation",
            "plural": True,
        },
        "cohesion": {"label": "cohesion", "plural": False},
        "vocabulary_grammar": {
            "label": "grammatical accuracy and language range",
            "plural": True,
        },
        "register": {
            "label": (
                "adapting tone and style appropriately to purpose, "
                "audience and context"
            ),
            "plural": False,
        },
    },
}


OVERALL_SUMMARY_NARRATIVES = {
    # -----------------------------------------------------
    # POSITIVE / AT-STANDARD OPENINGS
    # -----------------------------------------------------
    "all_strong": (
        "Overall, {learner_name} demonstrates particularly strong skills "
        "across all four assessed areas."
    ),
    "all_established": (
        "Overall, {learner_name}'s skills are well established across all "
        "four assessed areas."
    ),
    "all_satisfactory": (
        "Overall, {learner_name}'s skills satisfactorily meet the minimum "
        "expected standard across all four assessed areas."
    ),
    "positive_strong": (
        "Overall, {strong_subject} are particularly strong."
    ),
    "positive_established": (
        "Overall, {established_subject} are well established."
    ),
    "positive_satisfactory": (
        "Overall, {satisfactory_subject} satisfactorily meet the minimum "
        "expected standard for this level."
    ),
    "positive_strong_established": (
        "Overall, {strong_subject} are particularly strong, while "
        "{established_subject} are also well established."
    ),
    "positive_strong_satisfactory": (
        "Overall, {strong_subject} are particularly strong, while "
        "{satisfactory_subject} satisfactorily meet the minimum expected "
        "standard for this level."
    ),
    "positive_established_satisfactory": (
        "Overall, {established_subject} are well established, while "
        "{satisfactory_subject} satisfactorily meet the minimum expected "
        "standard for this level."
    ),
    "positive_strong_established_satisfactory": (
        "Overall, {strong_subject} are particularly strong, "
        "{established_subject} are well established, while "
        "{satisfactory_subject} satisfactorily meet the minimum expected "
        "standard for this level."
    ),

    # -----------------------------------------------------
    # ONE SKILL REQUIRING DEVELOPMENT
    # -----------------------------------------------------
    "one_uneven_developing": (
        "However, {skill} is more uneven, with {developing_areas} still "
        "developing."
    ),
    "one_all_developing": (
        "However, {skill} is still developing across all assessed areas and "
        "requires further consolidation to reach the minimum expected standard "
        "for this level."
    ),
    "one_uneven_needs_work": (
        "However, {skill} is more uneven, with {needs_work_areas} falling well "
        "below the minimum expected standard and requiring substantial further "
        "development."
    ),
    "one_uneven_needs_work_and_developing": (
        "However, {skill} is more uneven, with {needs_work_areas} falling well "
        "below the minimum expected standard and requiring substantial further "
        "development, while {developing_areas} {developing_verb} still "
        "developing."
    ),
    "one_below_standard_mixed": (
        "However, {skill} remains below the minimum expected standard overall, "
        "with {needs_work_areas} falling well below that standard and requiring "
        "substantial further development, while {developing_areas} "
        "{developing_verb} still developing."
    ),
    "one_all_needs_work": (
        "However, {skill} falls well below the minimum expected standard "
        "across all assessed areas and requires substantial further development."
    ),

    # -----------------------------------------------------
    # TWO OR THREE SKILLS REQUIRING DEVELOPMENT
    # -----------------------------------------------------
    "multiple_developing": (
        "However, {skills} include assessed areas that are still developing "
        "and have not yet reached the minimum expected standard."
    ),
    "multiple_needs_work": (
        "However, {skills} include assessed areas that fall well below the "
        "minimum expected standard and require substantial further development."
    ),
    "multiple_needs_work_and_developing": (
        "However, {skills} require further development, with some assessed "
        "areas still developing and others falling well below the minimum "
        "expected standard."
    ),

    # -----------------------------------------------------
    # ALL FOUR SKILLS CONTAIN LOWER-RATED AREAS
    # -----------------------------------------------------
    "all_four_developing": (
        "Overall, each of {learner_name}'s four language skills contains "
        "assessed areas that are still developing and have not yet reached "
        "the minimum expected standard."
    ),
    "all_four_needs_work": (
        "Overall, each of {learner_name}'s four language skills contains "
        "assessed areas that fall well below the minimum expected standard "
        "and require substantial further development."
    ),
    "all_four_needs_work_and_developing": (
        "Overall, each of {learner_name}'s four language skills contains "
        "areas requiring further development; some are still developing, "
        "while others fall well below the minimum expected standard."
    ),
}
