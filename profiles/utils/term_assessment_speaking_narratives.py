"""Canonical Speaking performance-summary narratives for Formal Term Assessment reports.

Tuple order is always:
fluency, accuracy_and_range, pronunciation, interaction.

Each of the 625 possible rating combinations has one explicit report narrative.
"""

SPEAKING_SUBSKILL_ORDER = (
    "fluency",
    "accuracy_and_range",
    "pronunciation",
    "interaction",
)

SPEAKING_PERFORMANCE_NARRATIVES = {
    ('needs_work', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} is still establishing the core abilities needed for effective spoken communication. '
        'Fluency, grammatical accuracy and language range, pronunciation and spoken interaction '
        'currently fall well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} shows developing ability in spoken interaction. However, fluency, grammatical accuracy '
        'and language range, as well as pronunciation, currently fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the minimum expected standard in spoken interaction.'
        'However, fluency, grammatical accuracy and language range, as well as pronunciation, '
        'currently fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} has proven to be rather confident in spoken interaction. '
        'However, fluency, grammatical accuracy, language range, as well as pronunciation, '
        'currently fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} is pretty strong in spoken interaction, displaying confidence and responsive '
        'participation in conversation. However, fluency, grammatical accuracy, language range, and '
        'pronunciation currently fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s pronunciation is still developing to reach this level's expectations, while fluency, grammatical accuracy, "
        'language range, and spoken interaction currently fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'developing'): (
        '{learner_name} shows developing abilities in pronunciation and spoken interaction. '
        'However, fluency, grammatical accuracy and language range fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level, while pronunciation is still "
        'developing. However, fluency as well as grammatical accuracy and language range fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates a fair amount of confidence in spoken interaction, while pronunciation is still '
        'developing. However, fluency as well as grammatical accuracy and language range fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction is fairly strong for this level, while pronunciation is still "
        'developing. However, fluency as well as grammatical accuracy and language range fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level. "
        "However, the other assessed speaking skills, such as fluency, grammatical accuracy "
        'and language range, and spoken interaction fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level, while spoken interaction is still "
        'developing. However, fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s pronunciation and spoken interaction meet the minimum expected "
        'standard for this level. However, fluency, grammatical accuracy and language range '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while pronunciation meets the minimum '
        'expected standard for this level. However, fluency, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while pronunciation meets the minimum '
        'expected standard for this level. However, fluency, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation. However, fluency and spoken interaction, '
        'together with grammatical accuracy and language range, currently fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction is still developing '
        'towards the minimum expected standard for this level. However, fluency, grammatical accuracy and '
        'language range fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction meets the minimum '
        'expected standard for this level. However, fluency, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in both pronunciation and spoken interaction. However, fluency, '
        'grammatical accuracy and language range fall well below the minimum expected standard for this level '
        'and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. However, fluency, grammatical accuracy and language range fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation. However, fluency and spoken interaction, '
        'together with grammatical accuracy and language range, currently fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction is still developing '
        'towards the minimum expected standard for this level. However, fluency, grammatical accuracy and '
        'language range fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction meets the minimum '
        'expected standard for this level. However, fluency, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and demonstrates confidence in spoken '
        'interaction. However, fluency, grammatical accuracy and language range fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in both pronunciation and spoken interaction. However, fluency, '
        'grammatical accuracy and language range fall well below the minimum expected standard for this level '
        'and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are developing but have not yet reached "
        'the minimum expected standard for this level. Fluency, pronunciation and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are developing "
        'but have not yet reached the minimum expected standard for this level. Fluency and pronunciation '
        'remain considerably below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level, while "
        'grammatical accuracy and language range are still developing. However, fluency and pronunciation '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'confident'): (
        '{learner_name} is confident in spoken interaction, while grammatical accuracy and language range '
        'are still developing towards the minimum expected standard for this level. Fluency and pronunciation '
        'remain considerably below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction skills are particularly strong. However, grammatical accuracy "
        'and language range are still developing, while fluency and pronunciation fall well below the '
        'minimum expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are developing but have "
        'not yet reached the minimum expected standard for this level. Fluency and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'are developing but have not yet reached the minimum expected standard for this level. '
        'Fluency remains the main area of difficulty, falling well below that standard and requiring '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level. "
        'Grammatical accuracy, language range and pronunciation are still developing, whereas fluency '
        'falls well below the required standard and needs substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'confident'): (
        '{learner_name} is confident in spoken interaction, while grammatical accuracy, language range '
        'and pronunciation are still developing towards the minimum expected standard for this level. '
        'Fluency remains substantially below that standard and requires considerable further development.'
    ),
    ('needs_work', 'developing', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction skills are particularly strong. In contrast, grammatical "
        'accuracy, language range and pronunciation are still developing and have not yet reached the '
        'minimum expected standard for this level. Fluency falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level, while "
        'grammatical accuracy and language range are still developing. However, fluency and spoken '
        'interaction fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level. "
        'Grammatical accuracy, language range and spoken interaction are still developing, while '
        'fluency falls well below the required standard and needs substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s pronunciation and spoken interaction meet the minimum expected standard "
        'for this level. Grammatical accuracy and language range are still developing and have not '
        'yet reached that standard, while fluency remains considerably below it and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} is confident in spoken interaction, and pronunciation meets the minimum '
        'expected standard for this level. Grammatical accuracy and language range are still '
        'developing, while fluency falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction skills are particularly strong, and pronunciation meets "
        'the minimum expected standard for this level. Grammatical accuracy and language range are '
        'still developing, whereas fluency falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confident control of pronunciation, while grammatical accuracy '
        'and language range are still developing. However, fluency and spoken interaction fall well '
        'below the minimum expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confident control of pronunciation, while grammatical accuracy, '
        'language range and spoken interaction are still developing and have not yet reached the '
        'minimum expected standard for this level. Fluency falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confident control of pronunciation, while spoken interaction '
        'meets the minimum expected standard for this level. Grammatical accuracy and language range '
        'are still developing, whereas fluency falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'confident', 'confident'): (
        '{learner_name} is confident in both pronunciation and spoken interaction. However, grammatical '
        'accuracy and language range are still developing and have not yet reached the minimum expected '
        'standard for this level. Fluency remains well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction skills are particularly strong, and pronunciation is also "
        'a confident area. However, grammatical accuracy and language range are still developing, while '
        'fluency falls well below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, although grammatical accuracy and "
        'language range are still developing and have not yet reached the minimum expected standard '
        'for this level. Fluency and spoken interaction fall well below that standard and require '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy, language "
        'range and spoken interaction are still developing towards the minimum expected standard for '
        'this level. Fluency falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, and spoken interaction meets the "
        'minimum expected standard for this level. Grammatical accuracy and language range are still '
        'developing, whereas fluency falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, and spoken interaction is also "
        'confident. However, grammatical accuracy and language range are still developing, while '
        'fluency falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly strong. "
        'In contrast, grammatical accuracy and language range are still developing and have not '
        'yet reached the minimum expected standard for this level. Fluency falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level. However, fluency, pronunciation and spoken interaction fall well below that '
        'standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level, while spoken interaction is still developing. However, fluency and pronunciation '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction meet the minimum "
        'expected standard for this level. In contrast, fluency and pronunciation fall well below that '
        'standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} is confident in spoken interaction, and grammatical accuracy and language range '
        'meet the minimum expected standard for this level. Fluency and pronunciation, however, fall well '
        'below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy "
        'and language range meet the minimum expected standard for this level. However, fluency and '
        'pronunciation remain well below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level, while pronunciation is still developing towards that standard. Fluency and '
        'spoken interaction remain well below it and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level. Pronunciation and spoken interaction are still developing and have not yet '
        'reached that standard, while fluency falls well below it and requires substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction meet the minimum "
        'expected standard for this level, while pronunciation is still developing. Fluency remains '
        'well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} is confident in spoken interaction, while grammatical accuracy and language '
        'range meet the minimum expected standard for this level. Pronunciation is still developing '
        'towards that standard, whereas fluency remains well below it and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, and grammatical "
        'accuracy and language range meet the minimum expected standard for this level. Pronunciation '
        'is still developing, while fluency remains well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation meet the minimum "
        'expected standard for this level. However, fluency and spoken interaction fall well below '
        'that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation meet the minimum "
        'expected standard for this level. Spoken interaction is still developing towards that '
        'standard, while fluency remains well below it and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'all meet the minimum expected standard for this level. Fluency, however, remains well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} is confident in spoken interaction, while grammatical accuracy, language '
        'range and pronunciation meet the minimum expected standard for this level. Fluency remains '
        'well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy, language range and pronunciation meet the minimum expected standard for this level. '
        'Fluency, however, remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and '
        'language range meet the minimum expected standard for this level. However, fluency and '
        'spoken interaction fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} is confident in pronunciation, and grammatical accuracy and language range '
        'meet the minimum expected standard for this level. Spoken interaction is still developing, '
        'whereas fluency remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy, '
        'language range and spoken interaction meet the minimum expected standard for this level. '
        'Fluency remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} is confident in both pronunciation and spoken interaction, while grammatical '
        'accuracy and language range meet the minimum expected standard for this level. However, '
        'fluency remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, and pronunciation "
        'is also an area of confidence. Grammatical accuracy and language range meet the minimum '
        'expected standard for this level, while fluency remains well below it and requires '
        'substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range meet the minimum expected standard for this level. Fluency and spoken '
        'interaction, however, fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, and grammatical accuracy and language "
        'range meet the minimum expected standard for this level. Spoken interaction is still developing, '
        'while fluency remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy, language "
        'range and spoken interaction meet the minimum expected standard for this level. Fluency remains '
        'well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, and spoken interaction is also an "
        'area of confidence. Grammatical accuracy and language range meet the minimum expected '
        'standard for this level, while fluency remains well below it and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly strong, "
        'while grammatical accuracy and language range meet the minimum expected standard for this '
        'level. Fluency, however, remains well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established. "
        'However, fluency, pronunciation and spoken interaction fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'spoken interaction is still developing towards the minimum expected standard for this level. '
        'Fluency and pronunciation fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while spoken "
        'interaction meets the minimum expected standard for this level. However, fluency and '
        'pronunciation fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in both grammatical accuracy and language range and '
        'spoken interaction. In contrast, fluency and pronunciation fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy and language range are also well established. However, fluency and pronunciation '
        'fall well below the minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while "
        'pronunciation is still developing towards the minimum expected standard for this level. '
        'Fluency and spoken interaction fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range. '
        'Pronunciation and spoken interaction are still developing and have not yet reached '
        'the minimum expected standard for this level, while fluency falls well below it '
        'and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, and spoken "
        'interaction meets the minimum expected standard for this level. Pronunciation is still '
        'developing, whereas fluency falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well '
        'as spoken interaction. Pronunciation is still developing towards the minimum expected '
        'standard for this level, while fluency remains well below it and requires substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy and language range are also well established. Pronunciation is still developing '
        'towards the minimum expected standard for this level, whereas fluency remains well below '
        'it and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation meets the minimum expected standard for this level. However, fluency and '
        'spoken interaction fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while "
        'pronunciation meets the minimum expected standard for this level. Spoken interaction '
        'is still developing, whereas fluency falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, '
        'while pronunciation and spoken interaction meet the minimum expected standard for '
        'this level. Fluency, however, remains well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range '
        'as well as spoken interaction, while pronunciation meets the minimum expected '
        'standard for this level. In contrast, fluency falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, and grammatical "
        'accuracy and language range are also well established. Pronunciation meets the minimum '
        'expected standard for this level, whereas fluency falls well below it and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range '
        'as well as pronunciation. However, fluency and spoken interaction fall well below '
        'the minimum expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well established. "
        'Spoken interaction is still developing towards the minimum expected standard for this level, '
        'while fluency falls well below it and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well '
        'as pronunciation, while spoken interaction meets the minimum expected standard for this '
        'level. Fluency remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'are all well established, with confidence evident across these three assessed areas. '
        'Fluency, however, falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy, language range and pronunciation are also well established. Fluency remains '
        'well below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range are also well established. However, fluency and spoken interaction fall '
        'well below the minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, and grammatical accuracy and "
        'language range are also well established. Spoken interaction is still developing, '
        'whereas fluency falls well below the minimum expected standard for this level '
        'and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy "
        'and language range are also well established. Spoken interaction meets the minimum '
        'expected standard for this level, whereas fluency remains well below it and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy, "
        'language range and spoken interaction are also well established. Fluency, however, '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly strong, "
        'while grammatical accuracy and language range are also well established. In contrast, '
        'fluency falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'However, fluency, pronunciation and spoken interaction fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'spoken interaction is still developing and has not yet reached the minimum expected '
        'standard for this level. Fluency and pronunciation fall well below that standard '
        'and require substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, and "
        'spoken interaction meets the minimum expected standard for this level. Fluency and '
        'pronunciation, however, fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'and spoken interaction is also well established. In contrast, fluency and pronunciation '
        'fall well below the minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities "
        'are particularly strong. However, fluency and pronunciation fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation is still developing towards the minimum expected standard for this level. '
        'Fluency and spoken interaction fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Pronunciation and spoken interaction are still developing and have not yet reached '
        'the minimum expected standard for this level, while fluency remains well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'while spoken interaction meets the minimum expected standard for this level. '
        'Pronunciation is still developing, whereas fluency falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'and spoken interaction is also an area of confidence. Pronunciation is still '
        'developing and has not yet reached the minimum expected standard for this level, '
        'while fluency falls well below it and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities "
        'are particularly strong. However, pronunciation is still developing and has not yet '
        'reached the minimum expected standard for this level, while fluency falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'while pronunciation meets the minimum expected standard for this level. However, '
        'fluency and spoken interaction fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'and pronunciation meets the minimum expected standard for this level. Spoken '
        'interaction is still developing, whereas fluency falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'while pronunciation and spoken interaction meet the minimum expected standard '
        'for this level. Fluency, however, falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'and spoken interaction is also well established. Pronunciation meets the minimum '
        'expected standard for this level, whereas fluency remains well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities "
        'are particularly strong, while pronunciation meets the minimum expected standard '
        'for this level. Fluency remains well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'and pronunciation is also well established. However, fluency and spoken interaction '
        'fall well below the minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'while pronunciation is also well established. Spoken interaction is still developing '
        'towards the minimum expected standard for this level, whereas fluency remains well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'and pronunciation is also an area of confidence. Spoken interaction meets the '
        'minimum expected standard for this level, while fluency falls well below it '
        'and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, "
        'with confidence also evident in pronunciation and spoken interaction. In contrast, '
        'fluency falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities "
        'are particularly strong, while pronunciation is also well established. Fluency, '
        'however, falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong. In contrast, fluency and spoken interaction fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong. Spoken interaction is still developing and has not yet reached the minimum '
        'expected standard for this level, while fluency falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while spoken interaction meets the minimum expected standard for this level. '
        'Fluency remains well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, and spoken interaction is also well established. Fluency, however, falls '
        'well below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'strong', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken "
        'interaction are particularly strong, demonstrating well-established abilities '
        'across all these assessed areas. Fluency, however, falls well below '
        'the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is developing but has not yet reached the minimum expected standard "
        'for this level. Grammatical accuracy and language range, pronunciation and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s fluency and spoken interaction are developing but have not yet reached "
        'the minimum expected standard for this level. Grammatical accuracy and language range, '
        'as well as pronunciation, fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level, "
        'while fluency is still developing. However, grammatical accuracy and language range, '
        'as well as pronunciation, fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} is confident in spoken interaction, while fluency is still developing '
        'towards the minimum expected standard for this level. Grammatical accuracy and language '
        'range, as well as pronunciation, fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, although fluency "
        'is still developing and has not yet reached the minimum expected standard for this level. '
        'Grammatical accuracy and language range, as well as pronunciation, fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are developing but have not yet reached "
        'the minimum expected standard for this level. Grammatical accuracy and language '
        'range, as well as spoken interaction, fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are developing, although "
        'none of these areas has yet reached the minimum expected standard for this level. '
        'Grammatical accuracy and language range remain well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level, "
        'while fluency and pronunciation are still developing. Grammatical accuracy and language '
        'range, however, fall well below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'confident'): (
        '{learner_name} is confident in spoken interaction, while fluency and pronunciation '
        'are still developing towards the minimum expected standard for this level. '
        'Grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, contrasting "
        'with the other assessed areas of speaking. Fluency and pronunciation are still '
        'developing, while grammatical accuracy and language range fall well below the '
        'minimum expected standard for this level and require substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level, "
        'while fluency is still developing. However, grammatical accuracy and language '
        'range, as well as spoken interaction, fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level, "
        'while fluency and spoken interaction are still developing. Grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s pronunciation and spoken interaction meet the minimum expected "
        'standard for this level. Fluency is still developing and has not yet reached '
        'that standard, while grammatical accuracy and language range fall well below '
        'it and require substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} is confident in spoken interaction, while pronunciation meets '
        'the minimum expected standard for this level. Fluency is still developing, '
        'whereas grammatical accuracy and language range fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'pronunciation meets the minimum expected standard for this level. Fluency is '
        'still developing, whereas grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s pronunciation is well established, while fluency is still "
        'developing towards the minimum expected standard for this level. However, '
        'grammatical accuracy and language range, as well as spoken interaction, '
        'fall well below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s pronunciation is well established, while fluency and spoken "
        'interaction are still developing and have not yet reached the minimum expected '
        'standard for this level. Grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} is confident in pronunciation, while spoken interaction meets '
        'the minimum expected standard for this level. Fluency is still developing, '
        'whereas grammatical accuracy and language range fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s pronunciation and spoken interaction are well established, "
        'with confidence evident in both areas. Fluency is still developing and has '
        'not yet reached the minimum expected standard for this level, while grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'pronunciation is also well established. However, fluency is still developing, '
        'and grammatical accuracy and language range fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is still "
        'developing towards the minimum expected standard for this level. Grammatical '
        'accuracy and language range, as well as spoken interaction, fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency and spoken "
        'interaction are still developing and have not yet reached the minimum expected '
        'standard for this level. Grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction "
        'meets the minimum expected standard for this level. Fluency is still developing, '
        'whereas grammatical accuracy and language range fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction "
        'is also well established. Fluency is still developing and has not yet reached '
        'the minimum expected standard for this level, whereas grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly "
        'strong. In contrast, fluency is still developing and has not yet reached the '
        'minimum expected standard for this level, while grammatical accuracy and '
        'language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are developing but have not yet "
        'reached the minimum expected standard for this level. Pronunciation and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are still "
        'developing and have not yet reached the minimum expected standard for this level. Pronunciation '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level, while "
        'fluency, grammatical accuracy and language range are still developing. Pronunciation, however, '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'confident'): (
        '{learner_name} is confident in spoken interaction, while fluency, grammatical accuracy and '
        'language range are still developing towards the minimum expected standard for this level. '
        'Pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, although fluency, "
        'grammatical accuracy and language range are still developing and have not yet reached the '
        'minimum expected standard for this level. Pronunciation falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are developing "
        'but have not yet reached the minimum expected standard for this level. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'developing', 'developing'): (
        "{learner_name}'s spoken communication abilities are still developing across all four assessed "
        'areas. Fluency, grammatical accuracy and language range, pronunciation and spoken interaction '
        'have not yet reached the minimum expected standard for this level and require further development.'
    ),
    ('developing', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s spoken interaction meets the minimum expected standard for this level. "
        'Fluency, grammatical accuracy, language range and pronunciation are still developing '
        'and require further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'developing', 'confident'): (
        '{learner_name} is confident in spoken interaction. However, fluency, grammatical accuracy, '
        'language range and pronunciation are still developing and have not yet reached the '
        'minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong. In contrast, "
        'fluency, grammatical accuracy, language range and pronunciation are still developing '
        'and require further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level, while "
        'fluency, grammatical accuracy and language range are still developing. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s pronunciation meets the minimum expected standard for this level. "
        'Fluency, grammatical accuracy, language range and spoken interaction are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s pronunciation and spoken interaction meet the minimum expected standard "
        'for this level. Fluency, grammatical accuracy and language range are still developing '
        'and require further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} is confident in spoken interaction, while pronunciation meets the '
        'minimum expected standard for this level. Fluency, grammatical accuracy and '
        'language range are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'pronunciation meets the minimum expected standard for this level. Fluency, '
        'grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s pronunciation is well established, while fluency, grammatical "
        'accuracy and language range are still developing towards the minimum expected '
        'standard for this level. Spoken interaction falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'developing', 'confident', 'developing'): (
        "{learner_name}'s pronunciation is well established, with confidence evident in this area. "
        'Fluency, grammatical accuracy, language range and spoken interaction are still developing '
        'and require further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} is confident in pronunciation, while spoken interaction meets the '
        'minimum expected standard for this level. Fluency, grammatical accuracy and '
        'language range are still developing and require further consolidation to '
        'reach that standard.'
    ),
    ('developing', 'developing', 'confident', 'confident'): (
        "{learner_name}'s pronunciation and spoken interaction are well established, with "
        'confidence evident in both areas. Fluency, grammatical accuracy and language range '
        'are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'developing', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'pronunciation is also well established. Fluency, grammatical accuracy and '
        'language range are still developing and have not yet reached the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical "
        'accuracy and language range are still developing towards the minimum expected '
        'standard for this level. Spoken interaction falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'developing', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong. However, fluency, grammatical "
        'accuracy, language range and spoken interaction are still developing and require '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction "
        'meets the minimum expected standard for this level. Fluency, grammatical accuracy '
        'and language range are still developing and require further consolidation to '
        'reach that standard.'
    ),
    ('developing', 'developing', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction "
        'is also well established. Fluency, grammatical accuracy and language range are '
        'still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'developing', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly "
        'strong. In contrast, fluency, grammatical accuracy and language range are still '
        'developing and have not yet reached the minimum expected standard for this level.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level, while fluency is still developing. However, pronunciation and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level. Fluency and spoken interaction are still developing and have not yet reached '
        'that standard, while pronunciation falls well below it and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction meet the minimum "
        'expected standard for this level. Fluency is still developing, whereas pronunciation falls '
        'well below that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} is confident in spoken interaction, while grammatical accuracy and language range '
        'meet the minimum expected standard for this level. Fluency is still developing, whereas pronunciation '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy "
        'and language range meet the minimum expected standard for this level. Fluency is still developing, '
        'whereas pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level, while fluency and pronunciation are still developing. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range meet the minimum expected standard "
        'for this level. Fluency, pronunciation and spoken interaction are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction meet the minimum "
        'expected standard for this level. Fluency and pronunciation are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while grammatical accuracy and language "
        'range meet the minimum expected standard for this level. Fluency and pronunciation are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy "
        'and language range meet the minimum expected standard for this level. Fluency and pronunciation '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation meet the minimum "
        'expected standard for this level. Fluency is still developing, whereas spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation meet the minimum "
        'expected standard for this level. Fluency and spoken interaction are still developing '
        'and require further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'all meet the minimum expected standard for this level. Fluency, however, is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} is confident in spoken interaction, while grammatical accuracy, language range '
        'and pronunciation meet the minimum expected standard for this level. Fluency is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy, "
        'language range and pronunciation meet the minimum expected standard for this level. Fluency '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s pronunciation is well established, while grammatical accuracy and language "
        'range meet the minimum expected standard for this level. Fluency is still developing, '
        'whereas spoken interaction falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s pronunciation is well established, while grammatical accuracy and language "
        'range meet the minimum expected standard for this level. Fluency and spoken interaction '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s pronunciation is well established, while grammatical accuracy, language "
        'range and spoken interaction meet the minimum expected standard for this level. Fluency '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s pronunciation and spoken interaction are well established, with confidence "
        'evident in both areas. Grammatical accuracy and language range meet the minimum expected '
        'standard for this level, while fluency is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while pronunciation "
        'is also well established. Grammatical accuracy and language range meet the minimum '
        'expected standard for this level, whereas fluency is still developing and requires '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range meet the minimum expected standard for this level. Fluency is still '
        'developing, whereas spoken interaction falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range meet the minimum expected standard for this level. Fluency and spoken '
        'interaction are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy, "
        'language range and spoken interaction meet the minimum expected standard for this level. '
        'Fluency is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction is also "
        'well established. Grammatical accuracy and language range meet the minimum expected '
        'standard for this level, whereas fluency is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly strong, "
        'while grammatical accuracy and language range meet the minimum expected standard for '
        'this level. Fluency is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'is still developing towards the minimum expected standard for this level. Pronunciation and '
        'spoken interaction fall well below that standard and require substantial further development.'
    ),
    ('developing', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'and spoken interaction are still developing and have not yet reached the minimum expected '
        'standard for this level. Pronunciation falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while spoken "
        'interaction meets the minimum expected standard for this level. Fluency is still developing, '
        'whereas pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are well established, "
        'with confidence evident in both assessed areas. Fluency is still developing towards the minimum '
        'expected standard for this level, while pronunciation falls well below it and requires substantial '
        'further development.'
    ),
    ('developing', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy "
        'and language range are also well established. Fluency is still developing, whereas pronunciation '
        'falls well below the minimum expected standard for this level and requires substantial further '
        'development.'
    ),
    ('developing', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'and pronunciation are still developing towards the minimum expected standard for this level. '
        'Spoken interaction falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established. However, fluency, "
        'pronunciation and spoken interaction are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while spoken "
        'interaction meets the minimum expected standard for this level. Fluency and pronunciation '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'developing', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are well established, "
        'with confidence evident in both assessed areas. Fluency and pronunciation are still developing '
        'and require further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy "
        'and language range are also well established. Fluency and pronunciation are still developing '
        'and require further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while pronunciation "
        'meets the minimum expected standard for this level. Fluency is still developing, whereas spoken '
        'interaction falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while pronunciation "
        'meets the minimum expected standard for this level. Fluency and spoken interaction are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while pronunciation "
        'and spoken interaction meet the minimum expected standard for this level. Fluency is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are well established, "
        'while pronunciation meets the minimum expected standard for this level. Fluency is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical accuracy "
        'and language range are also well established. Pronunciation meets the minimum expected standard '
        'for this level, whereas fluency is still developing and requires further consolidation to '
        'reach that standard.'
    ),
    ('developing', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well established, "
        'with confidence evident in both assessed areas. Fluency is still developing towards the '
        'minimum expected standard for this level, while spoken interaction falls well below it '
        'and requires substantial further development.'
    ),
    ('developing', 'confident', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well established. "
        'Fluency and spoken interaction are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well established, "
        'while spoken interaction meets the minimum expected standard for this level. Fluency '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'are all well established, with confidence evident across these three assessed areas. '
        'Fluency, however, is still developing and has not yet reached the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'confident', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy, language range and pronunciation are also well established. Fluency is still '
        'developing and requires further consolidation to reach the minimum expected standard '
        'for this level.'
    ),
    ('developing', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range are also well established. Fluency is still developing, whereas spoken '
        'interaction falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('developing', 'confident', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range are also well established. Fluency and spoken interaction are still '
        'developing and require further consolidation to reach the minimum expected standard '
        'for this level.'
    ),
    ('developing', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy and "
        'language range are also well established. Spoken interaction meets the minimum expected '
        'standard for this level, whereas fluency is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy, "
        'language range and spoken interaction are also well established. Fluency is still '
        'developing and requires further consolidation to reach the minimum expected standard '
        'for this level.'
    ),
    ('developing', 'confident', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly strong, "
        'while grammatical accuracy and language range are also well established. Fluency is '
        'still developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'is still developing towards the minimum expected standard for this level. Pronunciation and '
        'spoken interaction fall well below that standard and require substantial further development.'
    ),
    ('developing', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. Fluency and "
        'spoken interaction are still developing and have not yet reached the minimum expected standard '
        'for this level, while pronunciation falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction meets the minimum expected standard for this level. Fluency is still developing, '
        'whereas pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction is also well established. Fluency is still developing towards the minimum expected '
        'standard for this level, whereas pronunciation falls well below it and requires substantial '
        'further development.'
    ),
    ('developing', 'strong', 'needs_work', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities are "
        'particularly strong. In contrast, fluency is still developing and has not yet reached the '
        'minimum expected standard for this level, while pronunciation falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'and pronunciation are still developing towards the minimum expected standard for this level. '
        'Spoken interaction falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'strong', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. However, "
        'fluency, pronunciation and spoken interaction are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction meets the minimum expected standard for this level. Fluency and pronunciation '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'developing', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction is also well established. Fluency and pronunciation are still developing and '
        'require further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'developing', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities are "
        'particularly strong. However, fluency and pronunciation are still developing and require '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation meets the minimum expected standard for this level. Fluency is still '
        'developing, whereas spoken interaction falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation meets the minimum expected standard for this level. Fluency and spoken '
        'interaction are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation and spoken interaction meet the minimum expected standard for this level. '
        'Fluency is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, and spoken "
        'interaction is also well established. Pronunciation meets the minimum expected standard for '
        'this level, while fluency is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'strong', 'satisfactory', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities are "
        'particularly strong, while pronunciation meets the minimum expected standard for this level. '
        'Fluency is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation is also well established. Fluency is still developing, whereas spoken '
        'interaction falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('developing', 'strong', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation is also well established. Fluency and spoken interaction are still developing '
        'and require further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, and "
        'pronunciation is also well established. Spoken interaction meets the minimum expected '
        'standard for this level, while fluency is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, with "
        'confidence also evident in pronunciation and spoken interaction. Fluency, however, is '
        'still developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'strong', 'confident', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities "
        'are particularly strong, while pronunciation is also well established. Fluency is still '
        'developing and requires further consolidation to reach the minimum expected standard '
        'for this level.'
    ),
    ('developing', 'strong', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong. In contrast, fluency is still developing towards the minimum expected standard '
        'for this level, while spoken interaction falls well below it and requires substantial '
        'further development.'
    ),
    ('developing', 'strong', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong. Fluency and spoken interaction, however, are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while spoken interaction meets the minimum expected standard for this level. '
        'Fluency is still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while spoken interaction is also well established. Fluency remains below the '
        'minimum expected standard for this level and requires further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'abilities are particularly strong. Fluency, however, is still developing and has not yet '
        'reached the minimum expected standard for this level, requiring further consolidation.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency meets the minimum expected standard for this level. "
        'However, grammatical accuracy and language range, pronunciation and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s fluency meets the minimum expected standard for this level, while "
        'spoken interaction is still developing. Grammatical accuracy and language range, '
        'as well as pronunciation, fall well below that standard and require substantial '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency and spoken interaction meet the minimum expected standard "
        'for this level. However, grammatical accuracy and language range, as well as '
        'pronunciation, fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency meets the "
        'minimum expected standard for this level. In contrast, grammatical accuracy and '
        'language range, as well as pronunciation, fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency "
        'meets the minimum expected standard for this level. However, grammatical accuracy '
        'and language range, as well as pronunciation, fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s fluency meets the minimum expected standard for this level, while "
        'pronunciation is still developing. Grammatical accuracy and language range, as well '
        'as spoken interaction, fall well below that standard and require substantial '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s fluency meets the minimum expected standard for this level. "
        'Pronunciation and spoken interaction are still developing and have not yet reached '
        'that standard, while grammatical accuracy and language range fall well below it '
        'and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency and spoken interaction meet the minimum expected standard "
        'for this level. Pronunciation is still developing towards that standard, whereas '
        'grammatical accuracy and language range fall well below it and require substantial '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency meets the "
        'minimum expected standard for this level. Pronunciation is still developing, whereas '
        'grammatical accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency "
        'meets the minimum expected standard for this level. Pronunciation is still developing, '
        'whereas grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation meet the minimum expected standard for "
        'this level. However, grammatical accuracy and language range, as well as spoken '
        'interaction, fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency and pronunciation meet the minimum expected standard for "
        'this level, while spoken interaction is still developing. Grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction all meet the minimum "
        'expected standard for this level. However, grammatical accuracy and language range '
        'fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency and "
        'pronunciation meet the minimum expected standard for this level. Grammatical '
        'accuracy and language range, however, fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'fluency and pronunciation meet the minimum expected standard for this level. '
        'Grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s pronunciation is well established, while fluency meets the "
        'minimum expected standard for this level. However, grammatical accuracy and '
        'language range, as well as spoken interaction, fall well below that standard '
        'and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s pronunciation is well established, while fluency meets the "
        'minimum expected standard for this level. Spoken interaction is still developing, '
        'whereas grammatical accuracy and language range fall well below that standard '
        'and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s pronunciation is well established, while fluency and spoken "
        'interaction meet the minimum expected standard for this level. Grammatical '
        'accuracy and language range remain well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s pronunciation and spoken interaction are well established, "
        'with confidence evident in both areas. Fluency meets the minimum expected '
        'standard for this level, whereas grammatical accuracy and language range '
        'fall well below it and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'pronunciation is also well established. Fluency meets the minimum expected '
        'standard for this level, whereas grammatical accuracy and language range '
        'fall well below it and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency meets "
        'the minimum expected standard for this level. However, grammatical accuracy '
        'and language range, as well as spoken interaction, fall well below that '
        'standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency meets "
        'the minimum expected standard for this level. Spoken interaction is still '
        'developing, whereas grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency and spoken "
        'interaction meet the minimum expected standard for this level. Grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction "
        'is also well established. Fluency meets the minimum expected standard for '
        'this level, whereas grammatical accuracy and language range fall well below '
        'it and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly "
        'strong, while fluency meets the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency satisfactorily meets the minimum expected standard for this level, "
        'while grammatical accuracy and language range are still developing. Pronunciation and spoken '
        'interaction fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s fluency satisfactorily meets the minimum expected standard for this level. "
        'Grammatical accuracy, language range and spoken interaction are still developing and have not '
        'yet reached that standard, while pronunciation falls well below it and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency and spoken interaction satisfactorily meet the minimum expected "
        'standard for this level. Grammatical accuracy and language range are still developing, '
        'whereas pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency satisfactorily meets "
        'the minimum expected standard for this level. Grammatical accuracy and language range are '
        'still developing, whereas pronunciation falls well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy '
        'and language range are still developing, whereas pronunciation falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s fluency satisfactorily meets the minimum expected standard for this level, "
        'while grammatical accuracy, language range and pronunciation are still developing. Spoken '
        'interaction falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'developing'): (
        "{learner_name}'s fluency satisfactorily meets the minimum expected standard for this level. "
        'Grammatical accuracy, language range, pronunciation and spoken interaction are still developing '
        'and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency and spoken interaction satisfactorily meet the minimum expected "
        'standard for this level. Grammatical accuracy, language range and pronunciation are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'developing', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency satisfactorily "
        'meets the minimum expected standard for this level. Grammatical accuracy, language range '
        'and pronunciation are still developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy, '
        'language range and pronunciation are still developing and require further consolidation '
        'to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation satisfactorily meet the minimum expected "
        'standard for this level, while grammatical accuracy and language range are still '
        'developing. Spoken interaction falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency and pronunciation satisfactorily meet the minimum expected "
        'standard for this level. Grammatical accuracy, language range and spoken interaction '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction satisfactorily meet the "
        'minimum expected standard for this level. Grammatical accuracy and language range are '
        'still developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency and pronunciation "
        'satisfactorily meet the minimum expected standard for this level. Grammatical accuracy '
        'and language range are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency "
        'and pronunciation satisfactorily meet the minimum expected standard for this level. '
        'Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s pronunciation is well established, while fluency satisfactorily meets "
        'the minimum expected standard for this level. Grammatical accuracy and language range '
        'are still developing, whereas spoken interaction falls well below that standard and '
        'requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'confident', 'developing'): (
        "{learner_name}'s pronunciation is well established, while fluency satisfactorily meets "
        'the minimum expected standard for this level. Grammatical accuracy, language range and '
        'spoken interaction are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s pronunciation is well established, while fluency and spoken interaction "
        'satisfactorily meet the minimum expected standard for this level. Grammatical accuracy '
        'and language range are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'confident'): (
        "{learner_name}'s pronunciation and spoken interaction are well established, with "
        'confidence evident in both areas. Fluency satisfactorily meets the minimum expected '
        'standard for this level, while grammatical accuracy and language range are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while pronunciation "
        'is also well established. Fluency satisfactorily meets the minimum expected standard for '
        'this level, whereas grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency satisfactorily meets "
        'the minimum expected standard for this level. Grammatical accuracy and language range '
        'are still developing, whereas spoken interaction falls well below that standard and '
        'requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency satisfactorily meets "
        'the minimum expected standard for this level. Grammatical accuracy, language range and '
        'spoken interaction are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency and spoken interaction "
        'satisfactorily meet the minimum expected standard for this level. Grammatical accuracy '
        'and language range are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction is also "
        'well established. Fluency satisfactorily meets the minimum expected standard for this '
        'level, whereas grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly strong, "
        'while fluency satisfactorily meets the minimum expected standard for this level. '
        'Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range. However, pronunciation and spoken interaction fall well below '
        'that standard and require substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range, while spoken interaction is still developing. Pronunciation '
        'falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range, as well as spoken interaction. Pronunciation, however, falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency, grammatical "
        'accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level. Pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency, "
        'grammatical accuracy and language range satisfactorily meet the minimum expected standard '
        'for this level. Pronunciation remains well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range, while pronunciation is still developing. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range. Pronunciation and spoken interaction are still developing '
        'and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range, as well as spoken interaction. Pronunciation is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s spoken interaction is well established, while fluency, grammatical "
        'accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level. Pronunciation is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency, "
        'grammatical accuracy and language range satisfactorily meet the minimum expected standard '
        'for this level. Pronunciation is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range, as well as pronunciation. Spoken interaction, however, '
        'falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard in fluency, grammatical '
        'accuracy and language range, as well as pronunciation. Spoken interaction is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard across all four '
        'assessed areas of spoken communication. Fluency, grammatical accuracy and language '
        'range, pronunciation and spoken interaction are adequate for this level, although '
        'there is still considerable scope for further development and consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s spoken interaction is well established, with confidence evident in "
        'this area. Fluency, grammatical accuracy and language range, as well as pronunciation, '
        'satisfactorily meet the minimum expected standard for this level, with further scope '
        'for development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while fluency, "
        'grammatical accuracy and language range, as well as pronunciation, satisfactorily meet '
        'the minimum expected standard for this level, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s pronunciation is well established, while fluency, grammatical accuracy "
        'and language range satisfactorily meet the minimum expected standard for this level. '
        'Spoken interaction, however, falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s pronunciation is well established, while fluency, grammatical accuracy "
        'and language range satisfactorily meet the minimum expected standard for this level. '
        'Spoken interaction is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s pronunciation is well established, while fluency, grammatical accuracy "
        'and language range, as well as spoken interaction, satisfactorily meet the minimum '
        'expected standard for this level, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s pronunciation and spoken interaction are well established, with "
        'confidence evident in both areas. Fluency, grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level, although further '
        'consolidation would help strengthen these abilities.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'pronunciation is also well established. Fluency, grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level, with '
        'further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical "
        'accuracy and language range satisfactorily meet the minimum expected standard for '
        'this level. Spoken interaction falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical "
        'accuracy and language range satisfactorily meet the minimum expected standard for '
        'this level. Spoken interaction is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical "
        'accuracy and language range, as well as spoken interaction, satisfactorily meet '
        'the minimum expected standard for this level, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while spoken interaction "
        'is also well established. Fluency, grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level, with further '
        'scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly "
        'strong. Fluency, grammatical accuracy and language range satisfactorily meet the '
        'minimum expected standard for this level, although these areas would benefit '
        'from further consolidation and development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'satisfactorily meets the minimum expected standard for this level. However, pronunciation '
        'and spoken interaction fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Spoken interaction is still '
        'developing, whereas pronunciation falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'and spoken interaction satisfactorily meet the minimum expected standard for this level. '
        'Pronunciation, however, falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are well "
        'established, with confidence evident in both assessed areas. Fluency satisfactorily meets '
        'the minimum expected standard for this level, while pronunciation falls well below it '
        'and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy and language range are also well established. Fluency satisfactorily meets the '
        'minimum expected standard for this level, whereas pronunciation falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Pronunciation is still '
        'developing, whereas spoken interaction falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'confident', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Pronunciation and spoken '
        'interaction are still developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'and spoken interaction satisfactorily meet the minimum expected standard for this level. '
        'Pronunciation is still developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'developing', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are well "
        'established, with confidence evident in both assessed areas. Fluency satisfactorily meets '
        'the minimum expected standard for this level, while pronunciation is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy and language range are also well established. Fluency satisfactorily meets the '
        'minimum expected standard for this level, whereas pronunciation is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'and pronunciation satisfactorily meet the minimum expected standard for this level. '
        'Spoken interaction, however, falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency "
        'and pronunciation satisfactorily meet the minimum expected standard for this level. '
        'Spoken interaction is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, while fluency, "
        'pronunciation and spoken interaction satisfactorily meet the minimum expected standard '
        'for this level. These three areas would benefit from further consolidation to achieve '
        'greater consistency and confidence.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are well "
        'established, with confidence evident in both assessed areas. Fluency and pronunciation '
        'satisfactorily meet the minimum expected standard for this level, with further scope '
        'for development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while grammatical "
        'accuracy and language range are also well established. Fluency and pronunciation '
        'satisfactorily meet the minimum expected standard for this level, with further '
        'scope for development.'
    ),
    ('satisfactory', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well "
        'established, with confidence evident in both assessed areas. Fluency satisfactorily '
        'meets the minimum expected standard for this level, whereas spoken interaction '
        'falls well below it and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well "
        'established, with confidence evident in both assessed areas. Fluency satisfactorily '
        'meets the minimum expected standard for this level, while spoken interaction is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are well "
        'established, with confidence evident in both assessed areas. Fluency and spoken '
        'interaction satisfactorily meet the minimum expected standard for this level, '
        'with further scope for development.'
    ),
    ('satisfactory', 'confident', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken "
        'interaction are all well established, with confidence evident across these three '
        'assessed areas. Fluency satisfactorily meets the minimum expected standard for '
        'this level, although further consolidation would help strengthen this ability.'
    ),
    ('satisfactory', 'confident', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction abilities are particularly strong, while "
        'grammatical accuracy, language range and pronunciation are also well established. '
        'Fluency satisfactorily meets the minimum expected standard for this level, '
        'with further scope for development.'
    ),
    ('satisfactory', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy "
        'and language range are also well established. Fluency satisfactorily meets the '
        'minimum expected standard for this level, whereas spoken interaction falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy "
        'and language range are also well established. Fluency satisfactorily meets the '
        'minimum expected standard for this level, whereas spoken interaction is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy "
        'and language range are also well established. Fluency and spoken interaction '
        'satisfactorily meet the minimum expected standard for this level, with further '
        'scope for development.'
    ),
    ('satisfactory', 'confident', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while grammatical accuracy, "
        'language range and spoken interaction are also well established. Fluency '
        'satisfactorily meets the minimum expected standard for this level, although '
        'further consolidation would help strengthen this ability.'
    ),
    ('satisfactory', 'confident', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction abilities are particularly "
        'strong, while grammatical accuracy and language range are also well established. '
        'Fluency satisfactorily meets the minimum expected standard for this level, '
        'with further scope for development and consolidation.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'satisfactorily meets the minimum expected standard for this level. However, pronunciation and '
        'spoken interaction fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Spoken interaction is still '
        'developing, whereas pronunciation falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'and spoken interaction satisfactorily meet the minimum expected standard for this level. '
        'Pronunciation, however, falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction is also well established. Fluency satisfactorily meets the minimum expected standard '
        'for this level, whereas pronunciation falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities are "
        'particularly strong, while fluency satisfactorily meets the minimum expected standard for '
        'this level. Pronunciation, however, falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Pronunciation is still '
        'developing, whereas spoken interaction falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'strong', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'satisfactorily meets the minimum expected standard for this level. Pronunciation and spoken '
        'interaction are still developing and require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'and spoken interaction satisfactorily meet the minimum expected standard for this level. '
        'Pronunciation is still developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'developing', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction is also well established. Fluency satisfactorily meets the minimum expected '
        'standard for this level, whereas pronunciation is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'developing', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities are "
        'particularly strong, while fluency satisfactorily meets the minimum expected standard for '
        'this level. Pronunciation is still developing and requires further consolidation to '
        'reach that standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'and pronunciation satisfactorily meet the minimum expected standard for this level. '
        'Spoken interaction, however, falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency "
        'and pronunciation satisfactorily meet the minimum expected standard for this level. '
        'Spoken interaction is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency, "
        'pronunciation and spoken interaction satisfactorily meet the minimum expected standard for '
        'this level. These three areas would benefit from further consolidation to achieve greater '
        'consistency and confidence.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while spoken "
        'interaction is also well established. Fluency and pronunciation satisfactorily meet the '
        'minimum expected standard for this level, with further scope for development and consolidation.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities are "
        'particularly strong. Fluency and pronunciation satisfactorily meet the minimum expected '
        'standard for this level, although further consolidation would help strengthen these abilities.'
    ),
    ('satisfactory', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation is also well established. Fluency satisfactorily meets the minimum expected '
        'standard for this level, whereas spoken interaction falls well below that standard and '
        'requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation is also well established. Fluency satisfactorily meets the minimum expected '
        'standard for this level, whereas spoken interaction is still developing and requires '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while "
        'pronunciation is also well established. Fluency and spoken interaction satisfactorily '
        'meet the minimum expected standard for this level, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, with "
        'confidence also evident in pronunciation and spoken interaction. Fluency satisfactorily '
        'meets the minimum expected standard for this level, although further consolidation '
        'would help strengthen this ability.'
    ),
    ('satisfactory', 'strong', 'confident', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction abilities "
        'are particularly strong, while pronunciation is also well established. Fluency '
        'satisfactorily meets the minimum expected standard for this level, with further '
        'scope for development and consolidation.'
    ),
    ('satisfactory', 'strong', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while fluency satisfactorily meets the minimum expected standard for this level. '
        'Spoken interaction, however, falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'strong', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while fluency satisfactorily meets the minimum expected standard for this level. '
        'Spoken interaction is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'strong', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while fluency and spoken interaction satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development and consolidation.'
    ),
    ('satisfactory', 'strong', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly "
        'strong, while spoken interaction is also well established. Fluency satisfactorily meets '
        'the minimum expected standard for this level, although further consolidation would '
        'help strengthen this ability.'
    ),
    ('satisfactory', 'strong', 'strong', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range, pronunciation and spoken interaction "
        'abilities are particularly strong, demonstrating a high level of performance across three '
        'of the four assessed areas. Fluency satisfactorily meets the minimum expected standard '
        'for this level, although further consolidation would help strengthen this ability.'
    ),
    ('confident', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is well established. However, grammatical accuracy and language range, "
        'pronunciation and spoken interaction fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is well established, while spoken interaction is still developing. Grammatical "
        'accuracy and language range, together with pronunciation, fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is well established, and spoken interaction satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy and language range, as well as pronunciation, '
        'fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established. In contrast, grammatical accuracy "
        'and language range, along with pronunciation, fall well below the minimum expected standard for this '
        'level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency is also well established. "
        'However, grammatical accuracy and language range and pronunciation fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is well established, while pronunciation is still developing. Grammatical "
        'accuracy and language range, as well as spoken interaction, fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s fluency is well established. Pronunciation and spoken interaction are still developing "
        'and have not yet reached the minimum expected standard for this level, while grammatical accuracy and '
        'language range fall well below it and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is well established, and spoken interaction satisfactorily meets the minimum "
        'expected standard for this level. Pronunciation is still developing, whereas grammatical accuracy and '
        'language range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established, while pronunciation is still "
        'developing. Grammatical accuracy and language range fall well below the minimum expected standard for '
        'this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, with fluency also well established. "
        'Pronunciation is still developing, whereas grammatical accuracy and language range fall well below the '
        'minimum expected standard for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is well established, and pronunciation satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy and language range, as well as spoken '
        'interaction, fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is well established, while pronunciation satisfactorily meets the minimum "
        'expected standard for this level. Spoken interaction is still developing, whereas grammatical accuracy '
        'and language range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is well established, and both pronunciation and spoken interaction "
        'satisfactorily meet the minimum expected standard for this level. Grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established, while pronunciation "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency is well established and "
        'pronunciation satisfactorily meets the minimum expected standard for this level. Grammatical accuracy '
        'and language range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are well established. However, grammatical accuracy and "
        'language range and spoken interaction fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s fluency and pronunciation are well established, while spoken interaction is still "
        'developing. Grammatical accuracy and language range fall well below the minimum expected standard for '
        'this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are well established, and spoken interaction satisfactorily "
        'meets the minimum expected standard for this level. Grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are well established. Grammatical "
        'accuracy and language range, however, fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, and fluency and pronunciation are also well "
        'established. Grammatical accuracy and language range fall well below the minimum expected standard for '
        'this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is also well established. "
        'Grammatical accuracy and language range, as well as spoken interaction, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, and fluency is well established. Spoken "
        'interaction is still developing, whereas grammatical accuracy and language range fall well below the '
        'minimum expected standard for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is well established and spoken "
        'interaction satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and '
        'language range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency and spoken interaction are also "
        'well established. Grammatical accuracy and language range fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction are particularly strong, while fluency is also "
        'well established. Grammatical accuracy and language range fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy and language range are still "
        'developing. Pronunciation and spoken interaction fall well below the minimum expected standard for this '
        'level and require substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is well established. Grammatical accuracy, language range and spoken "
        'interaction are still developing and have not yet reached the minimum expected standard for this level, '
        'while pronunciation falls well below it and requires substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is well established, and spoken interaction satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy and language range are still developing, whereas '
        'pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established. Grammatical accuracy and language "
        'range are still developing, while pronunciation falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, and fluency is also well established. "
        'Grammatical accuracy and language range are still developing, whereas pronunciation falls well below '
        'the minimum expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy, language range and "
        'pronunciation are still developing. Spoken interaction falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('confident', 'developing', 'developing', 'developing'): (
        "{learner_name}'s fluency is well established. Grammatical accuracy, language range, pronunciation and "
        'spoken interaction are still developing and require further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('confident', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is well established, while spoken interaction satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy, language range and pronunciation are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'developing', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established. Grammatical accuracy, language "
        'range and pronunciation are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'developing', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency is also well established. "
        'Grammatical accuracy, language range and pronunciation are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is well established, and pronunciation satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy and language range are still developing, whereas '
        'spoken interaction falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is well established, while pronunciation satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy, language range and spoken interaction are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is well established, and pronunciation and spoken interaction satisfactorily "
        'meet the minimum expected standard for this level. Grammatical accuracy and language range are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established, while pronunciation "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, with fluency also well established and "
        'pronunciation satisfactorily meeting the minimum expected standard for this level. Grammatical accuracy '
        'and language range are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are well established, while grammatical accuracy and "
        'language range are still developing. Spoken interaction falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('confident', 'developing', 'confident', 'developing'): (
        "{learner_name}'s fluency and pronunciation are well established. Grammatical accuracy, language range "
        'and spoken interaction are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are well established, while spoken interaction "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'confident', 'confident'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are well established. Grammatical "
        'accuracy and language range are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'developing', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency and pronunciation are also "
        'well established. Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is also well established. "
        'Grammatical accuracy and language range are still developing, whereas spoken interaction falls well '
        'below the minimum expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'developing', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, with fluency also well established. Grammatical "
        'accuracy, language range and spoken interaction are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is well established and spoken "
        'interaction satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and '
        'language range are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency and spoken interaction are also "
        'well established. Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction are particularly strong, while fluency is also "
        'well established. Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Pronunciation and spoken interaction '
        'fall well below that standard and require substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is well established, and grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Spoken interaction is still '
        'developing, whereas pronunciation falls well below that standard and requires substantial further '
        'development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy, language range and spoken "
        'interaction satisfactorily meet the minimum expected standard for this level. Pronunciation falls well '
        'below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established, while grammatical accuracy and "
        'language range satisfactorily meet the minimum expected standard for this level. Pronunciation falls '
        'well below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, and fluency is also well established. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, whereas pronunciation falls well below that standard and requires substantial further '
        'development.'
    ),
    ('confident', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Pronunciation is still developing, '
        'whereas spoken interaction falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s fluency is well established, and grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Pronunciation and spoken interaction '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy, language range and spoken "
        'interaction satisfactorily meet the minimum expected standard for this level. Pronunciation is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established, while grammatical accuracy and "
        'language range satisfactorily meet the minimum expected standard for this level. Pronunciation is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, and fluency is also well established. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, while pronunciation is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy, language range and "
        'pronunciation satisfactorily meet the minimum expected standard for this level. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is well established, and grammatical accuracy, language range and "
        'pronunciation satisfactorily meet the minimum expected standard for this level. Spoken interaction is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is well established, while grammatical accuracy, language range, pronunciation "
        'and spoken interaction satisfactorily meet the minimum expected standard for this level. Further '
        'consolidation of these three areas would help strengthen their consistency.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency and spoken interaction are well established, while grammatical accuracy, "
        'language range and pronunciation satisfactorily meet the minimum expected standard for this level. '
        'These two areas have further scope for development and consolidation.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, with fluency also well established. "
        'Grammatical accuracy, language range and pronunciation satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development in both areas.'
    ),
    ('confident', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are well established, while grammatical accuracy and "
        'language range satisfactorily meet the minimum expected standard for this level. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s fluency and pronunciation are well established, while grammatical accuracy and "
        'language range satisfactorily meet the minimum expected standard for this level. Spoken interaction is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are well established, while grammatical accuracy, language "
        'range and spoken interaction satisfactorily meet the minimum expected standard for this level. Both of '
        'these areas have further scope for consolidation.'
    ),
    ('confident', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are well established, while grammatical "
        'accuracy and language range satisfactorily meet the minimum expected standard for this level, with '
        'further scope for development.'
    ),
    ('confident', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency and pronunciation are also "
        'well established. Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, with further scope for consolidation.'
    ),
    ('confident', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, and fluency is also well established. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, whereas spoken interaction falls well below that standard and requires substantial further '
        'development.'
    ),
    ('confident', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is well established and "
        'grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level. Spoken interaction is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('confident', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency is well established. Grammatical "
        'accuracy, language range and spoken interaction satisfactorily meet the minimum expected standard for '
        'this level, with further scope for development in both areas.'
    ),
    ('confident', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency and spoken interaction are also "
        'well established. Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, with further scope for consolidation.'
    ),
    ('confident', 'satisfactory', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction are particularly strong, while fluency is also "
        'well established. Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('confident', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established. However, "
        'pronunciation and spoken interaction fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, while spoken "
        'interaction is still developing. Pronunciation falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, while spoken "
        'interaction satisfactorily meets the minimum expected standard for this level. Pronunciation falls well '
        'below that standard and requires substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are well "
        'established, with confidence evident across these three assessed areas. Pronunciation falls well below '
        'the minimum expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency, grammatical accuracy and "
        'language range are also well established. Pronunciation falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, while "
        'pronunciation is still developing. Spoken interaction falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'developing', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established. Pronunciation "
        'and spoken interaction are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, while spoken "
        'interaction satisfactorily meets the minimum expected standard for this level. Pronunciation is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'confident', 'developing', 'confident'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are well "
        'established, while pronunciation is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('confident', 'confident', 'developing', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency, grammatical accuracy and "
        'language range are also well established. Pronunciation is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, while "
        'pronunciation satisfactorily meets the minimum expected standard for this level. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, and "
        'pronunciation satisfactorily meets the minimum expected standard for this level. Spoken interaction is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are well established, while "
        'pronunciation and spoken interaction satisfactorily meet the minimum expected standard for this level, '
        'with further scope for development in both areas.'
    ),
    ('confident', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are well "
        'established, while pronunciation satisfactorily meets the minimum expected standard for this level, '
        'with further scope for consolidation.'
    ),
    ('confident', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency, grammatical accuracy and "
        'language range are also well established. Pronunciation satisfactorily meets the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('confident', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are well established. "
        'Spoken interaction, however, falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('confident', 'confident', 'confident', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are well established. "
        'Spoken interaction is still developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('confident', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are well established, "
        'while spoken interaction satisfactorily meets the minimum expected standard for this level, with '
        'further scope for consolidation.'
    ),
    ('confident', 'confident', 'confident', 'confident'): (
        "{learner_name}'s spoken communication is well established across all four assessed areas. Fluency, "
        'grammatical accuracy and language range, pronunciation and spoken interaction demonstrate consistent '
        'confidence at this level.'
    ),
    ('confident', 'confident', 'confident', 'strong'): (
        "{learner_name}'s spoken interaction is particularly strong, while fluency, grammatical accuracy, "
        'language range and pronunciation are also well established, demonstrating confidence across the '
        'remaining three assessed areas.'
    ),
    ('confident', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical accuracy and language "
        'range are also well established. Spoken interaction falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'strong', 'developing'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical accuracy and language "
        'range are also well established. Spoken interaction is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical accuracy and language "
        'range are also well established. Spoken interaction satisfactorily meets the minimum expected standard '
        'for this level, with further scope for consolidation.'
    ),
    ('confident', 'confident', 'strong', 'confident'): (
        "{learner_name}'s pronunciation is particularly strong, while fluency, grammatical accuracy, language "
        'range and spoken interaction are also well established, with confidence evident across these three '
        'other assessed areas.'
    ),
    ('confident', 'confident', 'strong', 'strong'): (
        "{learner_name}'s pronunciation and spoken interaction are particularly strong, while fluency, "
        'grammatical accuracy and language range are also well established. Performance is secure across all '
        'four assessed areas of speaking.'
    ),
    ('confident', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is also "
        'well established. Pronunciation and spoken interaction fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established. Spoken interaction is still developing, whereas pronunciation falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established and spoken interaction satisfactorily meets the minimum expected standard for this level. '
        'Pronunciation falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency and "
        'spoken interaction are also well established. Pronunciation falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are particularly strong, "
        'while fluency is also well established. Pronunciation falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established and pronunciation is still developing. Spoken interaction falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'developing', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is also "
        'well established. Pronunciation and spoken interaction are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established and spoken interaction satisfactorily meets the minimum expected standard for this level. '
        'Pronunciation is still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'strong', 'developing', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency and "
        'spoken interaction are also well established. Pronunciation is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'developing', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are particularly strong, "
        'while fluency is also well established. Pronunciation is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established and pronunciation satisfactorily meets the minimum expected standard for this level. Spoken '
        'interaction falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established and pronunciation satisfactorily meets the minimum expected standard for this level. Spoken '
        'interaction is still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency is well "
        'established. Pronunciation and spoken interaction satisfactorily meet the minimum expected standard for '
        'this level, with further scope for consolidation.'
    ),
    ('confident', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency and "
        'spoken interaction are also well established. Pronunciation satisfactorily meets the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('confident', 'strong', 'satisfactory', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are particularly strong, "
        'while fluency is also well established. Pronunciation satisfactorily meets the minimum expected '
        'standard for this level, with further scope for consolidation.'
    ),
    ('confident', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency and "
        'pronunciation are also well established. Spoken interaction falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency and "
        'pronunciation are also well established. Spoken interaction is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency and "
        'pronunciation are also well established. Spoken interaction satisfactorily meets the minimum expected '
        'standard for this level, with further scope for consolidation.'
    ),
    ('confident', 'strong', 'confident', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong, while fluency, "
        'pronunciation and spoken interaction are also well established, with confidence evident across these '
        'three other assessed areas.'
    ),
    ('confident', 'strong', 'confident', 'strong'): (
        "{learner_name}'s grammatical accuracy, language range and spoken interaction are particularly strong, "
        'while fluency and pronunciation are also well established. Performance is secure across all four '
        'assessed areas of speaking.'
    ),
    ('confident', 'strong', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly strong, while "
        'fluency is also well established. Spoken interaction falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly strong, while "
        'fluency is also well established. Spoken interaction is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly strong, while "
        'fluency is well established. Spoken interaction satisfactorily meets the minimum expected standard for '
        'this level, with further scope for consolidation.'
    ),
    ('confident', 'strong', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy, language range and pronunciation are particularly strong, while "
        'fluency and spoken interaction are also well established. Performance is secure across all four '
        'assessed areas of speaking.'
    ),
    ('confident', 'strong', 'strong', 'strong'): (
        "{learner_name}'s grammatical accuracy and language range, pronunciation and spoken interaction are "
        'particularly strong, while fluency is also well established.'
    ),
    ('strong', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong. However, grammatical accuracy and language range, "
        'pronunciation and spoken interaction fall well below the minimum expected standard for this level '
        'and require substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while spoken interaction is still developing. "
        'Grammatical accuracy and language range, together with pronunciation, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, and spoken interaction satisfactorily meets the "
        'minimum expected standard for this level. Grammatical accuracy and language range, as well as '
        'pronunciation, fall well below that standard and require substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s fluency is particularly strong, with confidence also evident in spoken interaction. "
        'Grammatical accuracy and language range, as well as pronunciation, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong. In contrast, grammatical "
        'accuracy and language range, as well as pronunciation, fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation is still developing. "
        'Grammatical accuracy and language range and spoken interaction fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s fluency is particularly strong. Pronunciation and spoken interaction are still "
        'developing towards the minimum expected standard for this level, whereas grammatical accuracy and '
        'language range fall well below it and require substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, and spoken interaction satisfactorily meets the "
        'minimum expected standard for this level. Pronunciation is still developing, while grammatical '
        'accuracy and language range fall well below that standard and require substantial further '
        'development.'
    ),
    ('strong', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while spoken interaction is also well established. "
        'Pronunciation is still developing towards the minimum expected standard for this level, whereas '
        'grammatical accuracy and language range fall well below it and require substantial further '
        'development.'
    ),
    ('strong', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong. Pronunciation is still "
        'developing, while grammatical accuracy and language range fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation satisfactorily meets the "
        'minimum expected standard for this level. Grammatical accuracy and language range and spoken '
        'interaction fall well below that standard and require substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is particularly strong, and pronunciation satisfactorily meets the minimum "
        'expected standard for this level. Spoken interaction is still developing, whereas grammatical '
        'accuracy and language range fall well below that standard and require substantial further '
        'development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation and spoken interaction "
        'satisfactorily meet the minimum expected standard for this level. Grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency is particularly strong, and spoken interaction is also well established. "
        'Pronunciation satisfactorily meets the minimum expected standard for this level, whereas grammatical '
        'accuracy and language range fall well below it and require substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while pronunciation "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('strong', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation is also well established. "
        'Grammatical accuracy and language range and spoken interaction fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s fluency is particularly strong, and pronunciation is also well established. Spoken "
        'interaction is still developing towards the minimum expected standard for this level, whereas '
        'grammatical accuracy and language range fall well below it and require substantial further '
        'development.'
    ),
    ('strong', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, with pronunciation also well established. Spoken "
        'interaction satisfactorily meets the minimum expected standard for this level, while grammatical '
        'accuracy and language range fall well below that standard and require substantial further '
        'development.'
    ),
    ('strong', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation and spoken interaction are also "
        'well established. Grammatical accuracy and language range fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, with pronunciation also "
        'well established. Grammatical accuracy and language range fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are particularly strong. However, grammatical accuracy "
        'and language range, as well as spoken interaction, fall well below the minimum expected standard for '
        'this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while spoken interaction is "
        'still developing. Grammatical accuracy and language range fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while spoken interaction "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, with spoken interaction also "
        'well established. Grammatical accuracy and language range fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'strong'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are particularly strong. Grammatical "
        'accuracy and language range, however, fall well below the minimum expected standard for this level '
        'and require substantial further development.'
    ),

    ('strong', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range are "
        'still developing. Pronunciation and spoken interaction fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is particularly strong. Grammatical accuracy, language range and spoken "
        'interaction are still developing and have not yet reached the minimum expected standard for this '
        'level, while pronunciation falls well below it and requires substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, and spoken interaction satisfactorily meets the "
        'minimum expected standard for this level. Grammatical accuracy and language range are still '
        'developing, whereas pronunciation falls well below that standard and requires substantial further '
        'development.'
    ),
    ('strong', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s fluency is particularly strong, with confidence also evident in spoken interaction. "
        'Grammatical accuracy and language range are still developing, while pronunciation falls well below '
        'the minimum expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong. Grammatical accuracy and "
        'language range are still developing, whereas pronunciation falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'pronunciation are still developing. Spoken interaction falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'developing', 'developing'): (
        "{learner_name}'s fluency is particularly strong. Grammatical accuracy, language range, pronunciation "
        'and spoken interaction are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while spoken interaction satisfactorily meets the "
        'minimum expected standard for this level. Grammatical accuracy, language range and pronunciation are '
        'still developing and require further consolidation to reach that standard.'
    ),
    ('strong', 'developing', 'developing', 'confident'): (
        "{learner_name}'s fluency is particularly strong, and spoken interaction is also well established. "
        'Grammatical accuracy, language range and pronunciation are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'developing', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong. Grammatical accuracy, "
        'language range and pronunciation are still developing and require further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation satisfactorily meets the "
        'minimum expected standard for this level. Grammatical accuracy and language range are still '
        'developing, whereas spoken interaction falls well below that standard and requires substantial '
        'further development.'
    ),
    ('strong', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is particularly strong, and pronunciation satisfactorily meets the minimum "
        'expected standard for this level. Grammatical accuracy, language range and spoken interaction are '
        'still developing and require further consolidation to reach that standard.'
    ),
    ('strong', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation and spoken interaction "
        'satisfactorily meet the minimum expected standard for this level. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('strong', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency is particularly strong, with confidence also evident in spoken interaction. "
        'Pronunciation satisfactorily meets the minimum expected standard for this level, while grammatical '
        'accuracy and language range are still developing and require further consolidation to reach that '
        'standard.'
    ),
    ('strong', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while pronunciation "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('strong', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, and pronunciation is also well established. "
        'Grammatical accuracy and language range are still developing, whereas spoken interaction falls well '
        'below the minimum expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'confident', 'developing'): (
        "{learner_name}'s fluency is particularly strong, with pronunciation also well established. "
        'Grammatical accuracy, language range and spoken interaction are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation is also well established. "
        'Spoken interaction satisfactorily meets the minimum expected standard for this level, whereas '
        'grammatical accuracy and language range are still developing and require further consolidation to '
        'reach that standard.'
    ),
    ('strong', 'developing', 'confident', 'confident'): (
        "{learner_name}'s fluency is particularly strong, and pronunciation and spoken interaction are also "
        'well established. Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'confident', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, with pronunciation also "
        'well established. Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy and "
        'language range are still developing. Spoken interaction falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'strong', 'developing'): (
        "{learner_name}'s fluency and pronunciation are particularly strong. Grammatical accuracy, language "
        'range and spoken interaction are still developing and require further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while spoken interaction "
        'satisfactorily meets the minimum expected standard for this level. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('strong', 'developing', 'strong', 'confident'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, with spoken interaction also "
        'well established. Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'strong', 'strong'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are particularly strong. Grammatical "
        'accuracy and language range are still developing and require further consolidation to reach the '
        'minimum expected standard for this level.'
    ),

    ('strong', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Pronunciation and spoken '
        'interaction fall well below that standard and require substantial further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Spoken interaction is still '
        'developing, whereas pronunciation falls well below that standard and requires substantial further '
        'development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'spoken interaction satisfactorily meet the minimum expected standard for this level. Pronunciation '
        'falls well below that standard and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s fluency is particularly strong, with confidence also evident in spoken interaction. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, whereas pronunciation falls well below that standard and requires substantial further '
        'development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while grammatical accuracy "
        'and language range satisfactorily meet the minimum expected standard for this level. Pronunciation '
        'falls well below that standard and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Pronunciation is still developing, '
        'whereas spoken interaction falls well below that standard and requires substantial further '
        'development.'
    ),
    ('strong', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range "
        'satisfactorily meet the minimum expected standard for this level. Pronunciation and spoken '
        'interaction are still developing and require further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'spoken interaction satisfactorily meet the minimum expected standard for this level. Pronunciation '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s fluency is particularly strong, with spoken interaction also well established. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, while pronunciation is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('strong', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while grammatical accuracy "
        'and language range satisfactorily meet the minimum expected standard for this level. Pronunciation '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'pronunciation satisfactorily meet the minimum expected standard for this level. Spoken interaction, '
        'however, falls well below that standard and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'pronunciation satisfactorily meet the minimum expected standard for this level. Spoken interaction '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range, "
        'pronunciation and spoken interaction satisfactorily meet the minimum expected standard for this '
        'level. These three areas would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while spoken interaction is also well established. "
        'Grammatical accuracy, language range and pronunciation satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while grammatical accuracy, "
        'language range and pronunciation satisfactorily meet the minimum expected standard for this level, '
        'with further scope for development.'
    ),
    ('strong', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, with pronunciation also well established. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, whereas spoken interaction falls well below that standard and requires substantial further '
        'development.'
    ),
    ('strong', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation is also well established. "
        'Grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, and spoken interaction is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('strong', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation is also well established. "
        'Grammatical accuracy, language range and spoken interaction satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while pronunciation and spoken interaction are also "
        'well established. Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while pronunciation is also "
        'well established. Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy and "
        'language range satisfactorily meet the minimum expected standard for this level. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy and "
        'language range satisfactorily meet the minimum expected standard for this level. Spoken interaction '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy, "
        'language range and spoken interaction satisfactorily meet the minimum expected standard for this '
        'level, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, with spoken interaction also "
        'well established. Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'strong'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are particularly strong, while "
        'grammatical accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, with further scope for development.'
    ),

    ('strong', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range are "
        'also well established. Pronunciation and spoken interaction fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s fluency is particularly strong, with grammatical accuracy and language range also "
        'well established. Spoken interaction is still developing, whereas pronunciation falls well below the '
        'minimum expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range are "
        'also well established. Spoken interaction satisfactorily meets the minimum expected standard for '
        'this level, whereas pronunciation falls well below it and requires substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'spoken interaction are also well established. Pronunciation falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, with grammatical accuracy "
        'and language range also well established. Pronunciation falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, with grammatical accuracy and language range also "
        'well established. Pronunciation is still developing, while spoken interaction falls well below the '
        'minimum expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'developing', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range are "
        'also well established. Pronunciation and spoken interaction are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, with grammatical accuracy and language range also "
        'well established. Spoken interaction satisfactorily meets the minimum expected standard for this '
        'level, while pronunciation is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('strong', 'confident', 'developing', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'spoken interaction are also well established. Pronunciation is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'developing', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, with grammatical accuracy "
        'and language range also well established. Pronunciation is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range are "
        'also well established. Pronunciation satisfactorily meets the minimum expected standard for this '
        'level, whereas spoken interaction falls well below that standard and requires substantial further '
        'development.'
    ),
    ('strong', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency is particularly strong, with grammatical accuracy and language range also "
        'well established. Pronunciation satisfactorily meets the minimum expected standard for this level, '
        'while spoken interaction is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('strong', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy and language range are "
        'also well established. Pronunciation and spoken interaction satisfactorily meet the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'spoken interaction are also well established. Pronunciation satisfactorily meets the minimum '
        'expected standard for this level, with further scope for development.'
    ),
    ('strong', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, with grammatical accuracy "
        'and language range also well established. Pronunciation satisfactorily meets the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'pronunciation are also well established. Spoken interaction falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'confident', 'developing'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'pronunciation are also well established. Spoken interaction is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range and "
        'pronunciation are also well established. Spoken interaction satisfactorily meets the minimum '
        'expected standard for this level, with further scope for development.'
    ),
    ('strong', 'confident', 'confident', 'confident'): (
        "{learner_name}'s fluency is particularly strong, while grammatical accuracy, language range, "
        'pronunciation and spoken interaction are all well established. Performance is confident across these '
        'three other assessed areas.'
    ),
    ('strong', 'confident', 'confident', 'strong'): (
        "{learner_name}'s fluency and spoken interaction are particularly strong, while grammatical accuracy, "
        'language range and pronunciation are also well established. Performance is secure across all four '
        'assessed areas of speaking.'
    ),
    ('strong', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy and "
        'language range are also well established. Spoken interaction falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'strong', 'developing'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, with grammatical accuracy and "
        'language range also well established. Spoken interaction is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy and "
        'language range are also well established. Spoken interaction satisfactorily meets the minimum '
        'expected standard for this level, with further scope for development.'
    ),
    ('strong', 'confident', 'strong', 'confident'): (
        "{learner_name}'s fluency and pronunciation are particularly strong, while grammatical accuracy, "
        'language range and spoken interaction are also well established. Performance is secure across all '
        'four assessed areas of speaking.'
    ),
    ('strong', 'confident', 'strong', 'strong'): (
        "{learner_name}'s fluency, pronunciation and spoken interaction are particularly strong, while "
        'grammatical accuracy and language range are also well established. Performance is secure across all '
        'four assessed areas of speaking.'
    ),

    ('strong', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are particularly strong. "
        'Pronunciation and spoken interaction fall well below the minimum expected standard for this level '
        'and require substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are particularly strong. Spoken "
        'interaction is still developing, whereas pronunciation falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s fluency, grammatical accuracy and language range are particularly strong, while "
        'spoken interaction satisfactorily meets the minimum expected standard for this level. Pronunciation '
        'falls well below that standard and requires substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'spoken interaction is also well established. Pronunciation falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'strong'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are "
        'particularly strong. Pronunciation, however, falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('strong', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation is still developing. Spoken interaction falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'strong', 'developing', 'developing'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong. "
        'Pronunciation and spoken interaction are still developing and require further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('strong', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'spoken interaction satisfactorily meets the minimum expected standard for this level. Pronunciation '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'strong', 'developing', 'confident'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'spoken interaction is also well established. Pronunciation is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'strong', 'developing', 'strong'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are "
        'particularly strong. Pronunciation is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('strong', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation satisfactorily meets the minimum expected standard for this level. Spoken interaction '
        'falls well below that standard and requires substantial further development.'
    ),
    ('strong', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation satisfactorily meets the minimum expected standard for this level. Spoken interaction '
        'is still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation and spoken interaction satisfactorily meet the minimum expected standard for this '
        'level, with further scope for development.'
    ),
    ('strong', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'spoken interaction is also well established. Pronunciation satisfactorily meets the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'strong', 'satisfactory', 'strong'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are "
        'particularly strong, while pronunciation satisfactorily meets the minimum expected standard for this '
        'level, with further scope for development.'
    ),
    ('strong', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation is also well established. Spoken interaction falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'strong', 'confident', 'developing'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation is also well established. Spoken interaction is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation is also well established. Spoken interaction satisfactorily meets the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('strong', 'strong', 'confident', 'confident'): (
        "{learner_name}'s fluency and command of grammar and language range are particularly strong, while "
        'pronunciation and spoken interaction are also well established. Performance is secure across all '
        'four assessed areas of speaking.'
    ),
    ('strong', 'strong', 'confident', 'strong'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and spoken interaction are "
        'particularly strong, with pronunciation also well established. Performance is secure across all four '
        'assessed areas of speaking.'
    ),
    ('strong', 'strong', 'strong', 'needs_work'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are particularly "
        'strong. Spoken interaction falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'strong', 'strong', 'developing'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are particularly "
        'strong. Spoken interaction is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('strong', 'strong', 'strong', 'satisfactory'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are particularly "
        'strong, while spoken interaction satisfactorily meets the minimum expected standard for this level, '
        'with further scope for development.'
    ),
    ('strong', 'strong', 'strong', 'confident'): (
        "{learner_name}'s fluency, grammatical accuracy, language range and pronunciation are particularly "
        'strong, with spoken interaction also well established. Performance is secure across all four '
        'assessed areas of speaking.'
    ),
    ('strong', 'strong', 'strong', 'strong'): (
        "{learner_name}'s spoken communication is particularly strong across fluency, grammatical accuracy "
        'and language range, pronunciation and spoken interaction, with all four assessed areas firmly '
        'established for this level.'
    ),
}
