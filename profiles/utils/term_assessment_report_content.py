"""
Curated pedagogical content for Formal Term Assessment Reports.

Recommendations are selected from submitted assessment ratings.

This module contains content only; it does not access or modify the database.
"""


# ---------------------------------------------------------
# RATING INTERPRETATIONS
# ---------------------------------------------------------

RATING_INTERPRETATIONS = {
    "needs_work": "This area requires targeted development.",
    "developing": "This area is still developing.",
    "satisfactory": "Performance in this area is satisfactory.",
    "confident": "Performance in this area is confident and secure.",
    "strong": "Performance in this area is a clear strength.",
}


# ---------------------------------------------------------
# SUBSKILL RECOMMENDATIONS
#
# Keys must match the existing SUBSKILLS dictionary.
# Nested keys prevent collisions between subskills sharing
# identifiers, such as Reading and Listening: detailed.
# ---------------------------------------------------------

SUBSKILL_RECOMMENDATIONS = {
    "speaking": {
        "fluency": (
            "Develop greater continuity and ease when expressing ideas "
            "in spoken English, trying to reduce unnecessary hesitation."
        ),
        "accuracy_and_range": (
            "Strengthen grammatical accuracy and expand the range of "
            "vocabulary and sentence structures used in spoken communication."
        ),
        "pronunciation": (
            "Develop clearer pronunciation, word stress and intonation "
            "to support more effective spoken communication."
        ),
        "interaction": (
            "Strengthen conversational interaction through effective "
            "turn-taking, responding, asking follow-up questions and "
            "maintaining exchanges."
        ),
    },

    "reading": {
        "scanning": (
            "Develop the ability to locate specific information efficiently "
            "by trying to identify relevant keywords and details in written texts."
        ),
        "skimming": (
            "Strengthen the ability to identify the main idea and overall "
            "purpose of a text without relying on word-by-word reading."
        ),
        "detailed": (
            "Develop deeper understanding of written texts by interpreting "
            "supporting details, relationships between ideas and meaning "
            "in context."
        ),
    },

    "listening": {
        "gist": (
            "Strengthen the ability to identify the main message and "
            "overall purpose of spoken English without needing to "
            "understand every individual word."
        ),
        "specific_information": (
            "Develop the ability to recognise and retain specific details "
            "such as names, figures, dates and key information in spoken English."
        ),
        "detailed": (
            "Develop deeper comprehension of spoken English by recognising "
            "supporting details, connections between ideas and meaning "
            "in context."
        ),
    },

    "writing": {
        "organization": (
            "Strengthen the structure and organisation of written work "
            "through clear sequencing, paragraph development and "
            "appropriate presentation of ideas."
        ),
        "cohesion": (
            "Develop cohesion and coherence by connecting ideas logically "
            "and using appropriate linking expressions and referencing."
        ),
        "vocabulary_grammar": (
            "Improve grammatical accuracy and extend the range of "
            "vocabulary and sentence structures used in written communication."
        ),
        "register": (
            "Develop greater control of register by better adapting tone, style "
            "and language choices to the purpose, audience and context "
            "of written communication."
        ),
    },
}


# ---------------------------------------------------------
# PERFORMANCE SUMMARY — NARRATIVE EXPRESSIONS
#
# Used to construct natural, skill-by-skill report prose.
# These expressions are separate from the assessment labels
# and individual development recommendations.
# ---------------------------------------------------------

SUBSKILL_NARRATIVES = {
    "speaking": {
        "fluency": "speaking fluently and expressing ideas with ease",
        "accuracy_and_range": "using accurate grammar and a varied range of vocabulary and sentence structures",
        "pronunciation": "pronunciation, word stress and intonation",
        "interaction": "participating in conversations and maintaining exchanges",
    },

    "reading": {
        "scanning": "locating specific information in written texts",
        "skimming": "identifying the main ideas and overall purpose of a text",
        "detailed": "understanding detailed information and meaning in context",
    },

    "listening": {
        "gist": "understanding the main message and overall purpose of spoken English",
        "specific_information": "identifying specific information in spoken English",
        "detailed": "understanding detailed information and meaning in spoken English",
    },

    "writing": {
        "organization": "organising written work and presenting ideas clearly",
        "cohesion": "connecting ideas logically and maintaining coherence",
        "vocabulary_grammar": "using accurate grammar and a varied range of vocabulary and sentence structures",
        "register": "adapting tone and style to the purpose, audience and context",
    },
}


# ---------------------------------------------------------
# PERFORMANCE SUMMARY — RATING LANGUAGE
#
# Describes current demonstrated performance only.
# Development advice belongs in Development Priorities.
# ---------------------------------------------------------

NARRATIVE_RATING_LANGUAGE = {
    "needs_work": {
        "group": "development",
        "description": "currently shows limited ability",
    },
    "developing": {
        "group": "development",
        "description": "demonstrates developing ability",
    },
    "satisfactory": {
        "group": "satisfactory",
        "description": "demonstrates satisfactory ability",
    },
    "confident": {
        "group": "strength",
        "description": "demonstrates confidence",
    },
    "strong": {
        "group": "strength",
        "description": "demonstrates strong ability",
    },
}



# ---------------------------------------------------------
# PERFORMANCE SUMMARY — SPEAKING PROFILES
#
# Holistic narrative content for Speaking performance.
# Profile selection is handled in term_assessment_reports.py.
#
# Performance Summary describes demonstrated performance only.
# Development advice belongs in Development Priorities.
# ---------------------------------------------------------

SPEAKING_PROFILE_NARRATIVES = {
    "consistently_strong": {
        "all_confident": (
            "{learner_name} communicates confidently and effectively in spoken "
            "English, with secure performance across fluency, accuracy and range, "
            "pronunciation and interaction."
        ),
        "all_strong": (
            "Spoken communication is a clear strength for {learner_name}, who "
            "demonstrates consistently strong performance across fluency, accuracy "
            "and range, pronunciation and interaction."
        ),
        "mixed": {
            "opening_confident": (
                "{learner_name} communicates confidently and effectively in "
                "spoken English"
            ),
            "opening_strong": (
                "{learner_name} demonstrates a strong overall level of spoken "
                "communication"
            ),
            "strength_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "grammatical accuracy and language range",
                "pronunciation": "pronunciation",
                "interaction": "spoken interaction",
            },
            "secure_clause": {
                "fluency": "control of fluency",
                "accuracy_and_range": "grammatical and lexical control",
                "pronunciation": "control of pronunciation",
                "interaction": "interaction skills",
            },
        },
    },
    "generally_secure": {
        "all_satisfactory": (
            "{learner_name}'s spoken communication across fluency, accuracy and range, "
            "pronunciation and interaction is satisfactory for this level, although "
            "there remains considerable room for improvement across all assessed areas."
        ),        
        "mixed": {
            "opening_satisfactory": (
                "{learner_name} demonstrates a generally secure level of spoken communication"
            ),
            "opening_secure": (
                "{learner_name} communicates effectively in spoken English, with "
                "generally secure performance across the assessed areas"
            ),
            "confident_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "grammatical accuracy and language range",
                "pronunciation": "pronunciation",
                "interaction": "spoken interaction",
            },
            "satisfactory_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "accuracy and range",
                "pronunciation": "pronunciation",
                "interaction": "interaction",
            },
        },
    },
    "developing_evenly": {
        "all_developing": (
            "{learner_name}'s ability in spoken communication is still developing "
            "across all assessed areas. Fluency, accuracy and range, pronunciation "
            "and interaction all require further development to reach a satisfactory "
            "level of performance."
        ),        
        "mixed": {
            "opening_developing": (
                "{learner_name} demonstrates developing ability in spoken "
                "communication"
            ),
            "opening_satisfactory": (
                "{learner_name} demonstrates a developing but increasingly "
                "effective level of spoken communication"
            ),
            "satisfactory_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "language control",
                "pronunciation": "pronunciation",
                "interaction": "spoken interaction",
            },
            "developing_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "language control",
                "pronunciation": "pronunciation",
                "interaction": "spoken interaction",
            },
        },
    },
    "broad_support_needed": {
        "all_needs_work": (
            "{learner_name} currently demonstrates limited control across the main "
            "areas of spoken communication. Fluency, accuracy and range, pronunciation "
            "and interaction are not yet sufficiently established for consistently "
            "effective spoken communication."
        ),
        "mixed": {
            "opening_needs_work": (
                "{learner_name} is still establishing the core skills needed for "
                "effective spoken communication"
            ),
            "opening_developing": (
                "{learner_name} demonstrates emerging ability in spoken communication"
            ),
            "developing_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "language control",
                "pronunciation": "pronunciation",
                "interaction": "spoken interaction",
            },
            "needs_work_clause": {
                "fluency": "fluency",
                "accuracy_and_range": "language control",
                "pronunciation": "pronunciation",
                "interaction": "spoken interaction",
            },
        },
    },
    "pronounced_strength": {
        "baseline": {
            "needs_work": (
                "{learner_name} is still establishing the core skills needed for "
                "effective spoken communication"
            ),
            "developing": (
                "{learner_name} demonstrates developing ability in spoken communication"
            ),
            "satisfactory": (
                "{learner_name} demonstrates a generally satisfactory level of "
                "spoken communication"
            ),
            "confident": (
                "{learner_name} demonstrates a generally confident and secure level "
                "of spoken communication"
            ),
        },
        "standout": {
            "fluency": (
                "fluency stands out as a particular strength, allowing ideas to be "
                "expressed with greater continuity and ease"
            ),
            "accuracy_and_range": (
                "grammatical accuracy and language range stand out as particular "
                "strengths, supporting precise and flexible expression"
            ),
            "pronunciation": (
                "pronunciation stands out as a particular strength, supporting clear "
                "and effective spoken communication"
            ),
            "interaction": (
                "spoken interaction stands out as a particular strength, with confident "
                "and effective participation in conversational exchanges"
            ),
        },
        "secondary": {
            "fluency": "fluency is also relatively secure",
            "accuracy_and_range": "language control is also relatively secure",
            "pronunciation": "pronunciation is also relatively secure",
            "interaction": "spoken interaction is also relatively secure",
        },
        "baseline_area": {
            "fluency": "fluency",
            "accuracy_and_range": "language control",
            "pronunciation": "pronunciation",
            "interaction": "spoken interaction",
        },
    },
    "pronounced_weakness": {
        "baseline": {
            "developing": (
                "{learner_name} demonstrates developing ability in spoken communication"
            ),
            "satisfactory": (
                "{learner_name} demonstrates a generally satisfactory level of "
                "spoken communication"
            ),
            "confident": (
                "{learner_name} demonstrates a generally confident and secure level "
                "of spoken communication"
            ),
            "strong": (
                "{learner_name} demonstrates a strong overall level of spoken "
                "communication"
            ),
        },
        "contrast": {
            "fluency": (
                "fluency is notably less consistent, affecting the continuity and "
                "ease of spoken expression"
            ),
            "accuracy_and_range": (
                "language control is notably less secure, reducing precision and "
                "flexibility of expression"
            ),
            "pronunciation": (
                "pronunciation is notably less secure and can reduce the clarity "
                "of spoken communication"
            ),
            "interaction": (
                "spoken interaction is notably less secure, particularly when "
                "sustaining and responding within conversational exchanges"
            ),
        },
        "baseline_area": {
            "fluency": "fluency",
            "accuracy_and_range": "language control",
            "pronunciation": "pronunciation",
            "interaction": "spoken interaction",
        },
    },
    "mixed": {
        "opening": (
            "{learner_name} demonstrates an uneven profile in spoken communication, "
            "with clear differences in performance across the assessed areas."
        ),
        "area": {
            "fluency": "fluency",
            "accuracy_and_range": "language control",
            "pronunciation": "pronunciation",
            "interaction": "spoken interaction",
        },
        "stronger_effect": {
            "fluency": (
                "this supports greater continuity and ease when expressing ideas"
            ),
            "accuracy_and_range": (
                "this supports more precise and flexible expression"
            ),
            "pronunciation": (
                "this supports clarity and intelligibility in spoken communication"
            ),
            "interaction": (
                "this supports confident participation and the ability to sustain exchanges"
            ),
        },        
        "weaker_effect": {
            "fluency": (
                "this can make spoken expression less continuous and assured"
            ),
            "accuracy_and_range": (
                "this can reduce precision and flexibility when expressing ideas"
            ),
            "pronunciation": (
                "this can reduce clarity and intelligibility in spoken communication"
            ),
            "interaction": (
                "this can make conversational exchanges less sustained and responsive"
            ),
        },
    },
}



# READING_PROFILE_NARRATIVES = {
#     "area": {
#         "scanning": "locating specific information",
#         "skimming": "identifying main ideas and overall purpose",
#         "detailed": "understanding detailed information and meaning in context",
#     },
#     "all_strong": (
#         "{learner_name} demonstrates strong reading ability across all assessed "
#         "areas, with clear strengths in locating specific information, identifying "
#         "main ideas and overall purpose, and understanding detailed information "
#         "and meaning in context."
#     ),
#     "all_confident": (
#         "{learner_name} demonstrates confident and secure reading ability across "
#         "all assessed areas, including locating specific information, identifying "
#         "main ideas and overall purpose, and understanding detailed information "
#         "and meaning in context."
#     ),
#     "all_satisfactory": (
#         "{learner_name}'s reading performance across locating specific information, "
#         "identifying main ideas and overall purpose, and detailed comprehension is "
#         "satisfactory for this level, although there remains considerable room for "
#         "improvement across all assessed areas."
#     ),
#     "all_developing": (
#         "{learner_name}'s reading ability is still developing across all assessed "
#         "areas. Locating specific information, identifying main ideas and overall "
#         "purpose, and detailed comprehension all require further development to "
#         "reach a satisfactory level of performance."
#     ),
#     "all_needs_work": (
#         "{learner_name} currently experiences difficulty across all assessed areas "
#         "of reading. Locating specific information, identifying main ideas and "
#         "overall purpose, and detailed comprehension are not yet established at "
#         "the expected level."
#     ),
# }


# ---------------------------------------------------------
# DEVELOPMENT PRIORITIES — NARRATIVE RECOMMENDATIONS
#
# Supportive, learner-centred recommendations for each
# subskill. Used only when the rating is Needs Work or
# Developing.
# ---------------------------------------------------------

SUBSKILL_DEVELOPMENT_NARRATIVES = {
    "speaking": {
        "fluency": (
            "Practice should focus on expressing ideas more continuously "
            "and confidently while trying to reduce unnecessary hesitation."
        ),
        "accuracy_and_range": (
            "Continued practice should focus on gradually improving grammatical "
            "accuracy and expanding the range of vocabulary and sentence "
            "structures used in spoken communication."
        ),
        "pronunciation": (
            "Further practice should focus on developing clearer pronunciation, "
            "word stress and intonation to support more effective communication."
        ),
        "interaction": (
            "Practice should focus on developing greater confidence in "
            "conversational exchanges, including turn-taking, responding "
            "appropriately and asking follow-up questions."
        ),
    },

    "reading": {
        "scanning": (
            "Practice should focus on developing greater confidence in locating "
            "specific information by recognising relevant keywords and details "
            "in written texts."
        ),
        "skimming": (
            "Further practice should focus on identifying main ideas and the "
            "overall purpose of a text without relying on word-by-word reading."
        ),
        "detailed": (
            "Practice should focus on recognising supporting information, "
            "identifying connections between ideas and gradually developing "
            "a deeper understanding of meaning in context."
        ),
    },

    "listening": {
        "gist": (
            "Continued listening practice should focus on recognising the main "
            "message and overall purpose of spoken English without needing "
            "to understand every individual word."
        ),
        "specific_information": (
            "Practice should focus on developing greater confidence in identifying "
            "and retaining specific information, including names, figures, dates "
            "and other relevant details."
        ),
        "detailed": (
            "Further listening practice should focus on recognising supporting "
            "details, identifying connections between ideas and gradually "
            "developing a deeper understanding of spoken English."
        ),
    },

    "writing": {
        "organization": (
            "Practice should focus on developing clearer organisation, logical "
            "sequencing and more effective paragraph structure."
        ),
        "cohesion": (
            "Continued practice should focus on connecting ideas more naturally "
            "and developing greater confidence in using appropriate linking "
            "expressions and referencing."
        ),
        "vocabulary_grammar": (
            "Practice should focus on gradually expanding the variety of "
            "vocabulary and sentence structures used in written communication "
            "while working towards greater grammatical accuracy."
        ),
        "register": (
            "Further practice should focus on developing greater awareness of "
            "tone and style while learning to adapt written communication "
            "to different purposes, audiences and contexts."
        ),
    },
}


# ---------------------------------------------------------
# DEVELOPMENT PRIORITIES — SKILL CONSOLIDATION
#
# Used when no subskills within a skill are rated
# Needs Work or Developing.
# ---------------------------------------------------------

SKILL_CONSOLIDATION_NARRATIVES = {
    "speaking": (
        "No specific development priorities have been identified at this stage. "
        "Continued speaking practice is encouraged to consolidate existing "
        "skills and progressively extend confidence and communicative range."
    ),
    "reading": (
        "No specific development priorities have been identified at this stage. "
        "Continued exposure to varied written texts is encouraged to consolidate "
        "existing reading skills and progressively extend comprehension."
    ),
    "listening": (
        "No specific development priorities have been identified at this stage. "
        "Continued exposure to spoken English and regular listening practice "
        "are encouraged to consolidate existing skills and progressively "
        "extend comprehension."
    ),
    "writing": (
        "No specific development priorities have been identified at this stage. "
        "Continued writing practice is encouraged to consolidate existing "
        "skills and progressively extend accuracy, range and confidence."
    ),
}


# ---------------------------------------------------------
# DEVELOPMENT PRIORITIES — SATISFACTORY
#
# Used when a skill has no Needs Work or Developing
# ratings, but one or more subskills are rated
# Satisfactory (6/10).
# ---------------------------------------------------------

SKILL_SATISFACTORY_NARRATIVES = {
    "speaking": (
        "Performance is satisfactory, with opportunities to further develop "
        "fluency, accuracy and confidence in spoken communication. Continued "
        "speaking practice is encouraged to consolidate existing skills and "
        "gradually extend communicative range and flexibility."
    ),
    "reading": (
        "Performance is satisfactory, with opportunities to further develop "
        "reading efficiency and depth of comprehension. Continued exposure to "
        "varied written texts is encouraged to consolidate existing skills and "
        "support further progress."
    ),    
    "listening": (
        "Performance is satisfactory, with opportunities to further develop "
        "listening confidence and depth of comprehension. Regular exposure to "
        "spoken English is encouraged to consolidate existing skills and "
        "gradually strengthen comprehension across different speaking styles "
        "and contexts."
    ),
    "writing": (
        "Performance is satisfactory, with opportunities to further develop "
        "accuracy, range and flexibility in written communication. Continued "
        "writing practice is encouraged to consolidate existing skills and "
        "progressively strengthen the ability to express ideas clearly and "
        "effectively."
    ),
}


# ---------------------------------------------------------
# NEXT-TERM FOCUS — LEARNING OBJECTIVES
#
# Natural-language expressions used to generate the
# next learning period's recommended focus.
# ---------------------------------------------------------

SUBSKILL_NEXT_TERM_FOCUS = {
    "speaking": {
        "fluency": "developing greater fluency and confidence in spoken communication",
        "accuracy_and_range": "improving grammatical accuracy and extending vocabulary and sentence structure range in spoken communication",
        "pronunciation": "developing clearer pronunciation, word stress and intonation",
        "interaction": "strengthening conversational interaction and confidence in spoken exchanges",
    },

    "reading": {
        "scanning": "improving the ability to locate specific information efficiently in written texts",
        "skimming": "strengthening the ability to identify main ideas and the overall purpose of written texts",
        "detailed": "strengthening detailed reading comprehension",
    },

    "listening": {
        "gist": "developing greater confidence in understanding the main message of spoken English",
        "specific_information": "improving the ability to identify and retain specific information in spoken English",
        "detailed": "strengthening detailed listening comprehension",
    },

    "writing": {
        "organization": "developing clearer organisation and structure in written communication",
        "cohesion": "strengthening cohesion and the logical connection of ideas in writing",
        "vocabulary_grammar": "improving grammatical accuracy and vocabulary range in writing",
        "register": "developing greater flexibility in adapting written communication to different audiences and purposes",
    },
}

