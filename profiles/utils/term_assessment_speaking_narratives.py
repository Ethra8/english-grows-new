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
        '{learner_name} is still establishing the core skills needed for effective spoken communication. '
        'Fluency, grammatical accuracy and language range, pronunciation, and spoken interaction are not yet '
        'sufficiently established and require further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} shows developing ability in spoken interaction, while fluency, grammatical accuracy '
        'and language range, and pronunciation remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction. However, Fluency, grammatical '
        'accuracy and language range, and pronunciation remain less established and require further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction. However, Fluency, grammatical accuracy '
        'and language range, and pronunciation remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, supporting confident and responsive '
        'participation in conversation. However, Fluency, grammatical accuracy and language range, and '
        'pronunciation remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} shows developing ability in pronunciation, while fluency, grammatical accuracy and '
        'language range, and spoken interaction remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'developing'): (
        '{learner_name} shows developing ability in pronunciation and spoken interaction, while fluency as '
        'well as grammatical accuracy and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while pronunciation is still '
        'developing. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while pronunciation is still '
        'developing. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while pronunciation is still '
        'developing. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in pronunciation. However, Fluency, grammatical accuracy '
        'and language range, and spoken interaction remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in pronunciation, while spoken interaction is still '
        'developing. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in pronunciation and spoken interaction. However, Fluency '
        'as well as grammatical accuracy and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while pronunciation meets the expected '
        'standard. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while pronunciation meets the expected '
        'standard. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation. However, Fluency, grammatical accuracy and '
        'language range, and spoken interaction remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction is still '
        'developing. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction meets the expected '
        'standard. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction. However, Fluency as '
        'well as grammatical accuracy and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, supporting clarity and intelligibility. '
        'However, Fluency, grammatical accuracy and language range, and spoken interaction remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction is still '
        'developing. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction meets the expected '
        'standard. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. However, Fluency as well as grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction. However, Fluency as '
        'well as grammatical accuracy and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} shows developing ability in grammatical accuracy and language range, while fluency, '
        'pronunciation, and spoken interaction remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'developing'): (
        '{learner_name} shows developing ability in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency and pronunciation remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while grammatical accuracy and '
        'language range are still developing. However, Fluency and pronunciation remain less established and '
        'require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range are still developing. However, Fluency and pronunciation remain less established and '
        'require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range are still developing. However, Fluency and pronunciation remain less established and require '
        'further development.'
    ),
    ('needs_work', 'developing', 'developing', 'needs_work'): (
        '{learner_name} shows developing ability in grammatical accuracy and language range as well as '
        'pronunciation, while fluency and spoken interaction remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'developing', 'developing'): (
        '{learner_name} shows developing ability in grammatical accuracy and language range, pronunciation, '
        'and spoken interaction, while fluency remains less established and requires further development.'
    ),
    ('needs_work', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while grammatical accuracy and '
        'language range as well as pronunciation are still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range as well as pronunciation are still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range as well as pronunciation are still developing. However, Fluency remains less established and '
        'requires further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in pronunciation, while grammatical accuracy and language '
        'range are still developing. However, Fluency and spoken interaction remain less established and '
        'require further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction are still developing. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in pronunciation and spoken interaction, while '
        'grammatical accuracy and language range are still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while pronunciation meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while pronunciation meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range are still developing. However, Fluency and spoken interaction remain less established and '
        'require further development.'
    ),
    ('needs_work', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction are still developing. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while grammatical '
        'accuracy and language range are still developing. However, Fluency remains less established and '
        'requires further development.'
    ),
    ('needs_work', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Grammatical accuracy and language range are still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range are still developing. However, Fluency and spoken interaction remain less established and '
        'require further development.'
    ),
    ('needs_work', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction are still developing. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range are still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while grammatical '
        'accuracy and language range are still developing. However, Fluency remains less established and '
        'requires further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range. However, '
        'Fluency, pronunciation, and spoken interaction remain less established and require further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while spoken '
        'interaction is still developing. However, Fluency and pronunciation remain less established and '
        'require further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'spoken interaction. However, Fluency and pronunciation remain less established and require further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range meet the expected standard. However, Fluency and pronunciation remain less '
        'established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range meet the expected standard. However, Fluency and pronunciation remain less established and '
        'require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while '
        'pronunciation is still developing. However, Fluency and spoken interaction remain less established '
        'and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction are still developing. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'spoken interaction, while pronunciation is still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range meet the expected standard. Pronunciation is still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range meet the expected standard. Pronunciation is still developing; however, fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'pronunciation. However, Fluency and spoken interaction remain less established and require further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction is still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, '
        'pronunciation, and spoken interaction. However, Fluency remains less established and requires '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range as well as pronunciation meet the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range as well as pronunciation meet the expected standard. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. However, Fluency and spoken interaction remain less established '
        'and require further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. Spoken interaction is still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction meet the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while grammatical '
        'accuracy and language range meet the expected standard. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Grammatical accuracy and language range meet the expected standard; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. However, Fluency and spoken interaction remain less established '
        'and require further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. Spoken interaction is still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction meet the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range meet the expected standard; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while grammatical '
        'accuracy and language range meet the expected standard. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range. However, Fluency, '
        'pronunciation, and spoken interaction remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while spoken '
        'interaction is still developing. However, Fluency and pronunciation remain less established and '
        'require further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. However, Fluency and pronunciation remain less established '
        'and require further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction. However, Fluency and pronunciation remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. However, Fluency and pronunciation remain less established '
        'and require further development.'
    ),
    ('needs_work', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation is still developing. However, Fluency and spoken interaction remain less established '
        'and require further development.'
    ),
    ('needs_work', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction are still developing. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. Pronunciation is still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while pronunciation is still developing. However, Fluency remains less established and '
        'requires further development.'
    ),
    ('needs_work', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Pronunciation is still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. However, Fluency and spoken interaction remain less '
        'established and require further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. Spoken interaction is still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction meet the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while pronunciation meets the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Pronunciation meets the expected standard; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation. However, Fluency and spoken interaction remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction is still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction meets the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'confident', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, pronunciation, '
        'and spoken interaction. However, Fluency remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range as well as pronunciation. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. However, Fluency and spoken interaction remain less '
        'established and require further development.'
    ),
    ('needs_work', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Spoken interaction is still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Spoken interaction meets the expected standard; however, '
        'fluency remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range as well as spoken interaction. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction and also demonstrates '
        'confidence in grammatical accuracy and language range. However, Fluency remains less established and '
        'requires further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, supporting more '
        'precise and flexible expression. However, Fluency, pronunciation, and spoken interaction remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while spoken '
        'interaction is still developing. However, Fluency and pronunciation remain less established and '
        'require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. However, Fluency and pronunciation remain less established '
        'and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. However, Fluency and pronunciation remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction. However, Fluency and pronunciation remain less established and require further '
        'development.'
    ),
    ('needs_work', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation is still developing. However, Fluency and spoken interaction remain less established '
        'and require further development.'
    ),
    ('needs_work', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction are still developing. However, Fluency remains less established '
        'and requires further development.'
    ),
    ('needs_work', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. Pronunciation is still developing; however, fluency remains '
        'less established and requires further development.'
    ),
    ('needs_work', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Pronunciation is still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while pronunciation is still developing. However, Fluency remains less established and '
        'requires further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. However, Fluency and spoken interaction remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. Spoken interaction is still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction meet the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Pronunciation meets the expected standard; however, '
        'fluency remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while pronunciation meets the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. However, Fluency and spoken interaction remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Spoken interaction is still developing; however, fluency '
        'remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Spoken interaction meets the expected standard; however, '
        'fluency remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation and spoken interaction. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction and also demonstrates confidence in pronunciation. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation. However, Fluency and spoken interaction remain less established and require further '
        'development.'
    ),
    ('needs_work', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction is still developing. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction meets the expected standard. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation and also demonstrates confidence in spoken interaction. However, Fluency remains less '
        'established and requires further development.'
    ),
    ('needs_work', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range, pronunciation, and '
        'spoken interaction. However, Fluency remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} shows developing ability in fluency, while grammatical accuracy and language range, '
        'pronunciation, and spoken interaction remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} shows developing ability in fluency and spoken interaction, while grammatical '
        'accuracy and language range as well as pronunciation remain less established and require further '
        'development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while fluency is still developing. '
        'However, Grammatical accuracy and language range as well as pronunciation remain less established '
        'and require further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency is still developing. '
        'However, Grammatical accuracy and language range as well as pronunciation remain less established '
        'and require further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency is still developing. '
        'However, Grammatical accuracy and language range as well as pronunciation remain less established '
        'and require further development.'
    ),
    ('developing', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} shows developing ability in fluency and pronunciation, while grammatical accuracy and '
        'language range as well as spoken interaction remain less established and require further '
        'development.'
    ),
    ('developing', 'needs_work', 'developing', 'developing'): (
        '{learner_name} shows developing ability in fluency, pronunciation, and spoken interaction, while '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while fluency and pronunciation '
        'are still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency and pronunciation are '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency and pronunciation are '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in pronunciation, while fluency is still developing. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in pronunciation, while fluency and spoken interaction '
        'are still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in pronunciation and spoken interaction, while fluency is '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while pronunciation meets the expected '
        'standard. Fluency is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while pronunciation meets the expected '
        'standard. Fluency is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('developing', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency is still developing. However, '
        'Grammatical accuracy and language range as well as spoken interaction remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency and spoken interaction are '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction meets the expected '
        'standard. Fluency is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('developing', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while fluency is '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Fluency is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('developing', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency is still developing. However, '
        'Grammatical accuracy and language range as well as spoken interaction remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency and spoken interaction are '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('developing', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction meets the expected '
        'standard. Fluency is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('developing', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Fluency is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('developing', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while fluency is still '
        'developing. However, Grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('developing', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} shows developing ability in fluency as well as grammatical accuracy and language '
        'range, while pronunciation and spoken interaction remain less established and require further '
        'development.'
    ),
    ('developing', 'developing', 'needs_work', 'developing'): (
        '{learner_name} shows developing ability in fluency, grammatical accuracy and language range, and '
        'spoken interaction, while pronunciation remains less established and requires further development.'
    ),
    ('developing', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while fluency as well as '
        'grammatical accuracy and language range are still developing. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('developing', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency as well as grammatical '
        'accuracy and language range are still developing. However, Pronunciation remains less established '
        'and requires further development.'
    ),
    ('developing', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency as well as grammatical '
        'accuracy and language range are still developing. However, Pronunciation remains less established '
        'and requires further development.'
    ),
    ('developing', 'developing', 'developing', 'needs_work'): (
        '{learner_name} shows developing ability in fluency, grammatical accuracy and language range, and '
        'pronunciation, while spoken interaction remains less established and requires further development.'
    ),
    ('developing', 'developing', 'developing', 'developing'): (
        "{learner_name}'s ability in spoken communication is still developing across all assessed areas. "
        'Fluency, grammatical accuracy and language range, pronunciation, and spoken interaction all require '
        'further development to reach a satisfactory level of performance.'
    ),
    ('developing', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in spoken interaction, while fluency, grammatical '
        'accuracy and language range, and pronunciation are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction. However, Fluency, grammatical accuracy '
        'and language range, and pronunciation are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, supporting confident and responsive '
        'participation in conversation. However, Fluency, grammatical accuracy and language range, and '
        'pronunciation are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in pronunciation, while fluency as well as grammatical '
        'accuracy and language range are still developing. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('developing', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in pronunciation, while fluency, grammatical accuracy and '
        'language range, and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in pronunciation and spoken interaction, while fluency as '
        'well as grammatical accuracy and language range are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while pronunciation meets the expected '
        'standard. Fluency as well as grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while pronunciation meets the expected '
        'standard. Fluency as well as grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency as well as grammatical '
        'accuracy and language range are still developing. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('developing', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation. However, Fluency, grammatical accuracy and '
        'language range, and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while spoken interaction meets the expected '
        'standard. Fluency as well as grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction. However, Fluency as '
        'well as grammatical accuracy and language range are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Fluency as well as grammatical accuracy and language range are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency as well as grammatical '
        'accuracy and language range are still developing. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('developing', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, supporting clarity and intelligibility. '
        'However, Fluency, grammatical accuracy and language range, and spoken interaction are still '
        'developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while spoken interaction meets the expected '
        'standard. Fluency as well as grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Fluency as well as grammatical accuracy and language range are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction. However, Fluency as '
        'well as grammatical accuracy and language range are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while fluency '
        'is still developing. However, Pronunciation and spoken interaction remain less established and '
        'require further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while fluency '
        'and spoken interaction are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'spoken interaction, while fluency is still developing. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range meet the expected standard. Fluency is still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range meet the expected standard. Fluency is still developing; however, pronunciation remains less '
        'established and requires further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while fluency '
        'and pronunciation are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while '
        'fluency, pronunciation, and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'spoken interaction, while fluency and pronunciation are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range meet the expected standard. Fluency and pronunciation are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range meet the expected standard. Fluency and pronunciation are still developing and would benefit '
        'from further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'pronunciation, while fluency is still developing. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range as well as '
        'pronunciation, while fluency and spoken interaction are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, '
        'pronunciation, and spoken interaction, while fluency is still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while grammatical accuracy and '
        'language range as well as pronunciation meet the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while grammatical accuracy and language '
        'range as well as pronunciation meet the expected standard. Fluency is still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. Fluency is still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('developing', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. Fluency and spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction meet the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while grammatical '
        'accuracy and language range meet the expected standard. Fluency is still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Grammatical accuracy and language range meet the expected standard, while fluency is '
        'still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. Fluency is still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('developing', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range meet the expected standard. Fluency and spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while grammatical accuracy and language '
        'range as well as spoken interaction meet the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range meet the expected standard, while fluency is '
        'still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while grammatical '
        'accuracy and language range meet the expected standard. Fluency is still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency is '
        'still developing. However, Pronunciation and spoken interaction remain less established and require '
        'further development.'
    ),
    ('developing', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency and '
        'spoken interaction are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('developing', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. Fluency is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('developing', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency is still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('developing', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('developing', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency and '
        'pronunciation are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('developing', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range. However, Fluency, '
        'pronunciation, and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. Fluency and pronunciation are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction. However, Fluency and pronunciation are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency and pronunciation are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. Fluency is still developing; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('developing', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. Fluency and spoken interaction are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction meet the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while pronunciation meets the expected standard. Fluency is still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Pronunciation meets the expected standard, while fluency is '
        'still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while fluency is still developing. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('developing', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation. However, Fluency and spoken interaction are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction meets the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, pronunciation, '
        'and spoken interaction. However, Fluency is still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range as well as pronunciation. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency is still developing; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('developing', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency and spoken interaction are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Spoken interaction meets the expected standard, while '
        'fluency is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range as well as spoken interaction. Fluency is still developing '
        'and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction and also demonstrates '
        'confidence in grammatical accuracy and language range. Fluency is still developing and would benefit '
        'from further consolidation.'
    ),
    ('developing', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency is '
        'still developing. However, Pronunciation and spoken interaction remain less established and require '
        'further development.'
    ),
    ('developing', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency and '
        'spoken interaction are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('developing', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. Fluency is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('developing', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Fluency is still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('developing', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency is still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('developing', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency and '
        'pronunciation are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('developing', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, supporting more '
        'precise and flexible expression. However, Fluency, pronunciation, and spoken interaction are still '
        'developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while spoken '
        'interaction meets the expected standard. Fluency and pronunciation are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Fluency and pronunciation are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction. However, Fluency and pronunciation are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. Fluency is still developing; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('developing', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation meets the expected standard. Fluency and spoken interaction are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while '
        'pronunciation and spoken interaction meet the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Pronunciation meets the expected standard, while '
        'fluency is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while pronunciation meets the expected standard. Fluency is still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Fluency is still developing; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('developing', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Fluency and spoken interaction are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Spoken interaction meets the expected standard, while '
        'fluency is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation and spoken interaction. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction and also demonstrates confidence in pronunciation. Fluency is still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while fluency is still developing. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('developing', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation. However, Fluency and spoken interaction are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while spoken interaction meets the expected standard. Fluency is still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation and also demonstrates confidence in spoken interaction. Fluency is still developing '
        'and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range, pronunciation, and '
        'spoken interaction. However, Fluency is still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency. However, Grammatical accuracy and language '
        'range, pronunciation, and spoken interaction remain less established and require further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in fluency, while spoken interaction is still developing. '
        'However, Grammatical accuracy and language range as well as pronunciation remain less established '
        'and require further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency and spoken interaction. However, Grammatical '
        'accuracy and language range as well as pronunciation remain less established and require further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency meets the expected '
        'standard. However, Grammatical accuracy and language range as well as pronunciation remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency meets the expected '
        'standard. However, Grammatical accuracy and language range as well as pronunciation remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency, while pronunciation is still developing. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in fluency, while pronunciation and spoken interaction '
        'are still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency and spoken interaction, while pronunciation is '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency meets the expected '
        'standard. Pronunciation is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency meets the expected '
        'standard. Pronunciation is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency and pronunciation. However, Grammatical '
        'accuracy and language range as well as spoken interaction remain less established and require '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in fluency and pronunciation, while spoken interaction is '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency, pronunciation, and spoken interaction. '
        'However, Grammatical accuracy and language range remain less established and require further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency and pronunciation meet '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency and pronunciation meet '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency meets the expected standard. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency meets the expected standard. '
        'Spoken interaction is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency and spoken interaction meet '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while fluency meets '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Fluency meets the expected standard; however, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency meets the expected standard. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency meets the expected standard. '
        'Spoken interaction is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency and spoken interaction meet '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Fluency meets the expected standard; however, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while fluency meets '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency, while grammatical accuracy and language range '
        'are still developing. However, Pronunciation and spoken interaction remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in fluency, while grammatical accuracy and language range '
        'as well as spoken interaction are still developing. However, Pronunciation remains less established '
        'and requires further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency and spoken interaction, while grammatical '
        'accuracy and language range are still developing. However, Pronunciation remains less established '
        'and requires further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency, while grammatical accuracy and language range '
        'as well as pronunciation are still developing. However, Spoken interaction remains less established '
        'and requires further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in fluency, while grammatical accuracy and language '
        'range, pronunciation, and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency and spoken interaction, while grammatical '
        'accuracy and language range as well as pronunciation are still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency meets the expected '
        'standard. Grammatical accuracy and language range as well as pronunciation are still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency meets the expected '
        'standard. Grammatical accuracy and language range as well as pronunciation are still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency and pronunciation, while grammatical accuracy '
        'and language range are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in fluency and pronunciation, while grammatical accuracy '
        'and language range as well as spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency, pronunciation, and spoken interaction, while '
        'grammatical accuracy and language range are still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency and pronunciation meet '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency and pronunciation meet '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency meets the expected standard. '
        'Grammatical accuracy and language range are still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency meets the expected standard. '
        'Grammatical accuracy and language range as well as spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency and spoken interaction meet '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while fluency meets '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Fluency meets the expected standard, while grammatical accuracy and language range '
        'are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency meets the expected standard. '
        'Grammatical accuracy and language range are still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency meets the expected standard. '
        'Grammatical accuracy and language range as well as spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency and spoken interaction meet '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Fluency meets the expected standard, while grammatical accuracy and language range are '
        'still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while fluency meets '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency as well as grammatical accuracy and language '
        'range. However, Pronunciation and spoken interaction remain less established and require further '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in fluency as well as grammatical accuracy and language '
        'range, while spoken interaction is still developing. However, Pronunciation remains less established '
        'and requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency, grammatical accuracy and language range, and '
        'spoken interaction. However, Pronunciation remains less established and requires further '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency as well as grammatical accuracy and language '
        'range, while pronunciation is still developing. However, Spoken interaction remains less established '
        'and requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in fluency as well as grammatical accuracy and language '
        'range, while pronunciation and spoken interaction are still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in fluency, grammatical accuracy and language range, and '
        'spoken interaction, while pronunciation is still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in fluency, grammatical accuracy and language range, and '
        'pronunciation. However, Spoken interaction remains less established and requires further '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in fluency, grammatical accuracy and language range, and '
        'pronunciation, while spoken interaction is still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s spoken communication across fluency, grammatical accuracy and language range, "
        'pronunciation, and spoken interaction is satisfactory for this level, although there remains '
        'considerable room for improvement across all assessed areas.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in spoken interaction, while fluency, grammatical accuracy '
        'and language range, and pronunciation meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, supporting confident and responsive '
        'participation in conversation, while fluency, grammatical accuracy and language range, and '
        'pronunciation meet the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in pronunciation, while fluency, grammatical accuracy and '
        'language range, and spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in pronunciation and spoken interaction, while fluency as '
        'well as grammatical accuracy and language range meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'pronunciation. Fluency as well as grammatical accuracy and language range meet the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation, while fluency as well as grammatical '
        'accuracy and language range meet the expected standard. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation, supporting clarity and intelligibility, '
        'while fluency, grammatical accuracy and language range, and spoken interaction meet the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in spoken '
        'interaction. Fluency as well as grammatical accuracy and language range meet the expected standard, '
        'with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while fluency as well '
        'as grammatical accuracy and language range meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency '
        'meets the expected standard. However, Pronunciation and spoken interaction remain less established '
        'and require further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency '
        'meets the expected standard. Spoken interaction is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency and '
        'spoken interaction meet the expected standard. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency meets the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency meets the expected standard; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency '
        'meets the expected standard. Pronunciation is still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency '
        'meets the expected standard. Pronunciation and spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency and '
        'spoken interaction meet the expected standard. Pronunciation is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency meets the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency meets the expected standard, while pronunciation is '
        'still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency and '
        'pronunciation meet the expected standard. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency and '
        'pronunciation meet the expected standard. Spoken interaction is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while fluency, '
        'pronunciation, and spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency and pronunciation meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency and pronunciation meet the expected standard, with '
        'further scope for development.'
    ),
    ('satisfactory', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while fluency meets the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while fluency meets the expected standard. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range as well as '
        'pronunciation, while fluency and spoken interaction meet the expected standard, with further scope '
        'for development.'
    ),
    ('satisfactory', 'confident', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, pronunciation, '
        'and spoken interaction, while fluency meets the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'grammatical accuracy and language range as well as pronunciation. Fluency meets the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency meets the expected standard; however, spoken '
        'interaction remains less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency meets the expected standard, while spoken '
        'interaction is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range. Fluency and spoken interaction meet the expected standard, '
        'with further scope for development.'
    ),
    ('satisfactory', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in '
        'grammatical accuracy and language range as well as spoken interaction. Fluency meets the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction and also demonstrates '
        'confidence in grammatical accuracy and language range. Fluency meets the expected standard, with '
        'further scope for development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency '
        'meets the expected standard. However, Pronunciation and spoken interaction remain less established '
        'and require further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency '
        'meets the expected standard. Spoken interaction is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency and '
        'spoken interaction meet the expected standard. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Fluency meets the expected standard; however, '
        'pronunciation remains less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency meets the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency '
        'meets the expected standard. Pronunciation is still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency '
        'meets the expected standard. Pronunciation and spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency and '
        'spoken interaction meet the expected standard. Pronunciation is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Fluency meets the expected standard, while '
        'pronunciation is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency meets the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency and '
        'pronunciation meet the expected standard. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while fluency and '
        'pronunciation meet the expected standard. Spoken interaction is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, supporting more '
        'precise and flexible expression, while fluency, pronunciation, and spoken interaction meet the '
        'expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in spoken interaction. Fluency and pronunciation meet the expected standard, '
        'with further scope for development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while fluency and pronunciation meet the expected standard, with further scope for '
        'development.'
    ),
    ('satisfactory', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Fluency meets the expected standard; however, spoken '
        'interaction remains less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Fluency meets the expected standard, while spoken '
        'interaction is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation. Fluency and spoken interaction meet the expected standard, '
        'with further scope for development.'
    ),
    ('satisfactory', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in pronunciation and spoken interaction. Fluency meets the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction and also demonstrates confidence in pronunciation. Fluency meets the expected standard, '
        'with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while fluency meets the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while fluency meets the expected standard. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while fluency and spoken interaction meet the expected standard, with further scope '
        'for development.'
    ),
    ('satisfactory', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation and also demonstrates confidence in spoken interaction. Fluency meets the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range, pronunciation, and '
        'spoken interaction, while fluency meets the expected standard, with further scope for development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency. However, Grammatical accuracy and language range, '
        'pronunciation, and spoken interaction remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while spoken interaction is still developing. '
        'However, Grammatical accuracy and language range as well as pronunciation remain less established '
        'and require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while spoken interaction meets the expected '
        'standard. However, Grammatical accuracy and language range as well as pronunciation remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction. However, Grammatical '
        'accuracy and language range as well as pronunciation remain less established and require further '
        'development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. However, Grammatical accuracy and language range as well as pronunciation remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation is still developing. However, '
        'Grammatical accuracy and language range as well as spoken interaction remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation and spoken interaction are '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while spoken interaction meets the expected '
        'standard. Pronunciation is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('confident', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while pronunciation is '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Pronunciation is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation meets the expected standard. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation meets the expected standard. '
        'Spoken interaction is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation and spoken interaction meet '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while pronunciation meets '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Pronunciation meets the expected standard; however, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation. However, Grammatical accuracy '
        'and language range as well as spoken interaction remain less established and require further '
        'development.'
    ),
    ('confident', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while spoken interaction is '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while spoken interaction meets '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in fluency, pronunciation, and spoken interaction. However, '
        'Grammatical accuracy and language range remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency and pronunciation. However, Grammatical accuracy and language range remain less established '
        'and require further development.'
    ),
    ('confident', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Spoken interaction is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Spoken interaction meets the expected standard; however, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency '
        'and spoken interaction. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction and also demonstrates '
        'confidence in fluency. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range are '
        'still developing. However, Pronunciation and spoken interaction remain less established and require '
        'further development.'
    ),
    ('confident', 'developing', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range as '
        'well as spoken interaction are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('confident', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while spoken interaction meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('confident', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while grammatical accuracy '
        'and language range are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('confident', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Grammatical accuracy and language range are still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('confident', 'developing', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range as '
        'well as pronunciation are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('confident', 'developing', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in fluency. However, Grammatical accuracy and language range, '
        'pronunciation, and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('confident', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while spoken interaction meets the expected '
        'standard. Grammatical accuracy and language range as well as pronunciation are still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction. However, Grammatical '
        'accuracy and language range as well as pronunciation are still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Grammatical accuracy and language range as well as pronunciation are still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation meets the expected standard. '
        'Grammatical accuracy and language range are still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('confident', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation meets the expected standard. '
        'Grammatical accuracy and language range as well as spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while pronunciation and spoken interaction meet '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while pronunciation meets '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Pronunciation meets the expected standard, while grammatical accuracy and language range '
        'are still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while grammatical accuracy and '
        'language range are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('confident', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation. However, Grammatical accuracy '
        'and language range as well as spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('confident', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while spoken interaction meets '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in fluency, pronunciation, and spoken interaction. However, '
        'Grammatical accuracy and language range are still developing and would benefit from further '
        'consolidation.'
    ),
    ('confident', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency and pronunciation. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Grammatical accuracy and language range are still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('confident', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Grammatical accuracy and language range as well as spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Spoken interaction meets the expected standard, while grammatical accuracy and language range are '
        'still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency '
        'and spoken interaction. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction and also demonstrates '
        'confidence in fluency. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range '
        'meet the expected standard. However, Pronunciation and spoken interaction remain less established '
        'and require further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range '
        'meet the expected standard. Spoken interaction is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range as '
        'well as spoken interaction meet the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while grammatical accuracy '
        'and language range meet the expected standard. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Grammatical accuracy and language range meet the expected standard; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range '
        'meet the expected standard. Pronunciation is still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range '
        'meet the expected standard. Pronunciation and spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range as '
        'well as spoken interaction meet the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while grammatical accuracy '
        'and language range meet the expected standard. Pronunciation is still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Grammatical accuracy and language range meet the expected standard, while pronunciation is '
        'still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range as '
        'well as pronunciation meet the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range as '
        'well as pronunciation meet the expected standard. Spoken interaction is still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, while grammatical accuracy and language range, '
        'pronunciation, and spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in fluency and spoken interaction, while grammatical accuracy '
        'and language range as well as pronunciation meet the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency. Grammatical accuracy and language range as well as pronunciation meet the expected '
        'standard, with further scope for development.'
    ),
    ('confident', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while grammatical accuracy and '
        'language range meet the expected standard. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('confident', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while grammatical accuracy and '
        'language range meet the expected standard. Spoken interaction is still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency and pronunciation, while grammatical accuracy and '
        'language range as well as spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in fluency, pronunciation, and spoken interaction, while '
        'grammatical accuracy and language range meet the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency and pronunciation. Grammatical accuracy and language range meet the expected standard, with '
        'further scope for development.'
    ),
    ('confident', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Grammatical accuracy and language range meet the expected standard; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Grammatical accuracy and language range meet the expected standard, while spoken interaction is '
        'still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency. '
        'Grammatical accuracy and language range as well as spoken interaction meet the expected standard, '
        'with further scope for development.'
    ),
    ('confident', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency '
        'and spoken interaction. Grammatical accuracy and language range meet the expected standard, with '
        'further scope for development.'
    ),
    ('confident', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction and also demonstrates '
        'confidence in fluency. Grammatical accuracy and language range meet the expected standard, with '
        'further scope for development.'
    ),
    ('confident', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range. However, Pronunciation and spoken interaction remain less established and require further '
        'development.'
    ),
    ('confident', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while spoken interaction is still developing. However, Pronunciation remains less established '
        'and requires further development.'
    ),
    ('confident', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while spoken interaction meets the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('confident', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in fluency, grammatical accuracy and language range, and '
        'spoken interaction. However, Pronunciation remains less established and requires further '
        'development.'
    ),
    ('confident', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency as well as grammatical accuracy and language range. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('confident', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while pronunciation is still developing. However, Spoken interaction remains less established '
        'and requires further development.'
    ),
    ('confident', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range. However, Pronunciation and spoken interaction are still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while spoken interaction meets the expected standard. Pronunciation is still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in fluency, grammatical accuracy and language range, and '
        'spoken interaction. However, Pronunciation is still developing and would benefit from further '
        'consolidation.'
    ),
    ('confident', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency as well as grammatical accuracy and language range. Pronunciation is still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while pronunciation meets the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('confident', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while pronunciation meets the expected standard. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency as well as grammatical accuracy and language '
        'range, while pronunciation and spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in fluency, grammatical accuracy and language range, and '
        'spoken interaction, while pronunciation meets the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction and also demonstrates confidence in '
        'fluency as well as grammatical accuracy and language range. Pronunciation meets the expected '
        'standard, with further scope for development.'
    ),
    ('confident', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in fluency, grammatical accuracy and language range, and '
        'pronunciation. However, Spoken interaction remains less established and requires further '
        'development.'
    ),
    ('confident', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in fluency, grammatical accuracy and language range, and '
        'pronunciation. However, Spoken interaction is still developing and would benefit from further '
        'consolidation.'
    ),
    ('confident', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in fluency, grammatical accuracy and language range, and '
        'pronunciation, while spoken interaction meets the expected standard, with further scope for '
        'development.'
    ),
    ('confident', 'confident', 'confident', 'confident'): (
        '{learner_name} communicates confidently and effectively in spoken English, with secure performance '
        'across fluency, grammatical accuracy and language range, pronunciation, and spoken interaction.'
    ),
    ('confident', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in spoken interaction, while confidence is evident in fluency, '
        'grammatical accuracy and language range, and pronunciation.'
    ),
    ('confident', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency '
        'as well as grammatical accuracy and language range. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('confident', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency '
        'as well as grammatical accuracy and language range. Spoken interaction is still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in pronunciation and also demonstrates confidence in fluency '
        'as well as grammatical accuracy and language range. Spoken interaction meets the expected standard, '
        'with further scope for development.'
    ),
    ('confident', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in pronunciation, while confidence is evident in fluency, '
        'grammatical accuracy and language range, and spoken interaction.'
    ),
    ('confident', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in pronunciation and spoken interaction, while confidence is '
        'evident in fluency as well as grammatical accuracy and language range.'
    ),
    ('confident', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. However, Pronunciation and spoken interaction remain less '
        'established and require further development.'
    ),
    ('confident', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Spoken interaction is still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('confident', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Spoken interaction meets the expected standard; however, '
        'pronunciation remains less established and requires further development.'
    ),
    ('confident', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency and spoken interaction. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('confident', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction and also demonstrates confidence in fluency. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('confident', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Pronunciation is still developing; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('confident', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Pronunciation and spoken interaction are still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Spoken interaction meets the expected standard, while '
        'pronunciation is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency and spoken interaction. Pronunciation is still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction and also demonstrates confidence in fluency. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('confident', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Pronunciation meets the expected standard; however, spoken '
        'interaction remains less established and requires further development.'
    ),
    ('confident', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Pronunciation meets the expected standard, while spoken '
        'interaction is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency. Pronunciation and spoken interaction meet the expected standard, '
        'with further scope for development.'
    ),
    ('confident', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency and spoken interaction. Pronunciation meets the expected '
        'standard, with further scope for development.'
    ),
    ('confident', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction and also demonstrates confidence in fluency. Pronunciation meets the expected standard, '
        'with further scope for development.'
    ),
    ('confident', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency and pronunciation. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('confident', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency and pronunciation. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also '
        'demonstrates confidence in fluency and pronunciation. Spoken interaction meets the expected '
        'standard, with further scope for development.'
    ),
    ('confident', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while confidence '
        'is evident in fluency, pronunciation, and spoken interaction.'
    ),
    ('confident', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as spoken '
        'interaction, while confidence is evident in fluency and pronunciation.'
    ),
    ('confident', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation and also demonstrates confidence in fluency. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('confident', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation and also demonstrates confidence in fluency. Spoken interaction is still developing '
        'and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation and also demonstrates confidence in fluency. Spoken interaction meets the expected '
        'standard, with further scope for development.'
    ),
    ('confident', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range as well as '
        'pronunciation, while confidence is evident in fluency and spoken interaction.'
    ),
    ('confident', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range, pronunciation, and '
        'spoken interaction, while confidence is evident in fluency.'
    ),
    ('strong', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, supporting smoother and more continuous '
        'expression. However, Grammatical accuracy and language range, pronunciation, and spoken interaction '
        'remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while spoken interaction is still developing. '
        'However, Grammatical accuracy and language range as well as pronunciation remain less established '
        'and require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while spoken interaction meets the expected '
        'standard. However, Grammatical accuracy and language range as well as pronunciation remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. However, Grammatical accuracy and language range as well as pronunciation remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction. However, Grammatical '
        'accuracy and language range as well as pronunciation remain less established and require further '
        'development.'
    ),
    ('strong', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation is still developing. However, '
        'Grammatical accuracy and language range as well as spoken interaction remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation and spoken interaction are '
        'still developing. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while spoken interaction meets the expected '
        'standard. Pronunciation is still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('strong', 'needs_work', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Pronunciation is still developing; however, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while pronunciation is still '
        'developing. However, Grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation meets the expected standard. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation meets the expected standard. '
        'Spoken interaction is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation and spoken interaction meet '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Pronunciation meets the expected standard; however, grammatical accuracy and language '
        'range remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while pronunciation meets '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'However, Grammatical accuracy and language range as well as spoken interaction remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Spoken interaction is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Spoken interaction meets the expected standard; however, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation '
        'and spoken interaction. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction and also demonstrates '
        'confidence in pronunciation. However, Grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('strong', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency and pronunciation. However, Grammatical accuracy and '
        'language range as well as spoken interaction remain less established and require further '
        'development.'
    ),
    ('strong', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while spoken interaction is still '
        'developing. However, Grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while spoken interaction meets '
        'the expected standard. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in fluency and pronunciation and also demonstrates confidence '
        'in spoken interaction. However, Grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in fluency, pronunciation, and spoken interaction. However, '
        'Grammatical accuracy and language range remain less established and require further development.'
    ),
    ('strong', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range are '
        'still developing. However, Pronunciation and spoken interaction remain less established and require '
        'further development.'
    ),
    ('strong', 'developing', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range as '
        'well as spoken interaction are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('strong', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while spoken interaction meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('strong', 'developing', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range are still developing; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('strong', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while grammatical accuracy '
        'and language range are still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('strong', 'developing', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range as '
        'well as pronunciation are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('strong', 'developing', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in fluency, supporting smoother and more continuous '
        'expression. However, Grammatical accuracy and language range, pronunciation, and spoken interaction '
        'are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while spoken interaction meets the expected '
        'standard. Grammatical accuracy and language range as well as pronunciation are still developing and '
        'would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range as well as pronunciation are still developing '
        'and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction. However, Grammatical '
        'accuracy and language range as well as pronunciation are still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation meets the expected standard. '
        'Grammatical accuracy and language range are still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('strong', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation meets the expected standard. '
        'Grammatical accuracy and language range as well as spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while pronunciation and spoken interaction meet '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Pronunciation meets the expected standard, while grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while pronunciation meets '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Grammatical accuracy and language range are still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('strong', 'developing', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Grammatical accuracy and language range as well as spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Spoken interaction meets the expected standard, while grammatical accuracy and language range are '
        'still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation '
        'and spoken interaction. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction and also demonstrates '
        'confidence in pronunciation. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while grammatical accuracy and '
        'language range are still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('strong', 'developing', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in fluency and pronunciation. However, Grammatical accuracy and '
        'language range as well as spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while spoken interaction meets '
        'the expected standard. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in fluency and pronunciation and also demonstrates confidence '
        'in spoken interaction. Grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in fluency, pronunciation, and spoken interaction. However, '
        'Grammatical accuracy and language range are still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range meet '
        'the expected standard. However, Pronunciation and spoken interaction remain less established and '
        'require further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range meet '
        'the expected standard. Spoken interaction is still developing; however, pronunciation remains less '
        'established and requires further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range as '
        'well as spoken interaction meet the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range meet the expected standard; however, '
        'pronunciation remains less established and requires further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while grammatical accuracy '
        'and language range meet the expected standard. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('strong', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range meet '
        'the expected standard. Pronunciation is still developing; however, spoken interaction remains less '
        'established and requires further development.'
    ),
    ('strong', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range meet '
        'the expected standard. Pronunciation and spoken interaction are still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range as '
        'well as spoken interaction meet the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range meet the expected standard, while pronunciation '
        'is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while grammatical accuracy '
        'and language range meet the expected standard. Pronunciation is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range as '
        'well as pronunciation meet the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in fluency, while grammatical accuracy and language range as '
        'well as pronunciation meet the expected standard. Spoken interaction is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency, supporting smoother and more continuous '
        'expression, while grammatical accuracy and language range, pronunciation, and spoken interaction '
        'meet the expected standard, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in spoken '
        'interaction. Grammatical accuracy and language range as well as pronunciation meet the expected '
        'standard, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while grammatical accuracy '
        'and language range as well as pronunciation meet the expected standard, with further scope for '
        'development.'
    ),
    ('strong', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Grammatical accuracy and language range meet the expected standard; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('strong', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Grammatical accuracy and language range meet the expected standard, while spoken interaction is '
        'still developing and would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation. '
        'Grammatical accuracy and language range as well as spoken interaction meet the expected standard, '
        'with further scope for development.'
    ),
    ('strong', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in pronunciation '
        'and spoken interaction. Grammatical accuracy and language range meet the expected standard, with '
        'further scope for development.'
    ),
    ('strong', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction and also demonstrates '
        'confidence in pronunciation. Grammatical accuracy and language range meet the expected standard, '
        'with further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while grammatical accuracy and '
        'language range meet the expected standard. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('strong', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while grammatical accuracy and '
        'language range meet the expected standard. Spoken interaction is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while grammatical accuracy and '
        'language range as well as spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('strong', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in fluency and pronunciation and also demonstrates confidence '
        'in spoken interaction. Grammatical accuracy and language range meet the expected standard, with '
        'further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in fluency, pronunciation, and spoken interaction, while '
        'grammatical accuracy and language range meet the expected standard, with further scope for '
        'development.'
    ),
    ('strong', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. However, Pronunciation and spoken interaction remain less established '
        'and require further development.'
    ),
    ('strong', 'confident', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Spoken interaction is still developing; however, pronunciation remains '
        'less established and requires further development.'
    ),
    ('strong', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Spoken interaction meets the expected standard; however, pronunciation '
        'remains less established and requires further development.'
    ),
    ('strong', 'confident', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range as well as spoken interaction. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('strong', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction and also demonstrates '
        'confidence in grammatical accuracy and language range. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('strong', 'confident', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Pronunciation is still developing; however, spoken interaction remains '
        'less established and requires further development.'
    ),
    ('strong', 'confident', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Pronunciation and spoken interaction are still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Spoken interaction meets the expected standard, while pronunciation is '
        'still developing and would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range as well as spoken interaction. Pronunciation is still developing and '
        'would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction and also demonstrates '
        'confidence in grammatical accuracy and language range. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Pronunciation meets the expected standard; however, spoken interaction '
        'remains less established and requires further development.'
    ),
    ('strong', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Pronunciation meets the expected standard, while spoken interaction is '
        'still developing and would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range. Pronunciation and spoken interaction meet the expected standard, with '
        'further scope for development.'
    ),
    ('strong', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range as well as spoken interaction. Pronunciation meets the expected '
        'standard, with further scope for development.'
    ),
    ('strong', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction and also demonstrates '
        'confidence in grammatical accuracy and language range. Pronunciation meets the expected standard, '
        'with further scope for development.'
    ),
    ('strong', 'confident', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range as well as pronunciation. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('strong', 'confident', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range as well as pronunciation. Spoken interaction is still developing and '
        'would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in fluency and also demonstrates confidence in grammatical '
        'accuracy and language range as well as pronunciation. Spoken interaction meets the expected '
        'standard, with further scope for development.'
    ),
    ('strong', 'confident', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in fluency, while confidence is evident in grammatical '
        'accuracy and language range, pronunciation, and spoken interaction.'
    ),
    ('strong', 'confident', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in fluency and spoken interaction, while confidence is evident '
        'in grammatical accuracy and language range as well as pronunciation.'
    ),
    ('strong', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency and pronunciation and also demonstrates confidence '
        'in grammatical accuracy and language range. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('strong', 'confident', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in fluency and pronunciation and also demonstrates confidence '
        'in grammatical accuracy and language range. Spoken interaction is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency and pronunciation and also demonstrates confidence '
        'in grammatical accuracy and language range. Spoken interaction meets the expected standard, with '
        'further scope for development.'
    ),
    ('strong', 'confident', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in fluency and pronunciation, while confidence is evident in '
        'grammatical accuracy and language range as well as spoken interaction.'
    ),
    ('strong', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in fluency, pronunciation, and spoken interaction, while '
        'confidence is evident in grammatical accuracy and language range.'
    ),
    ('strong', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range. '
        'However, Pronunciation and spoken interaction remain less established and require further '
        'development.'
    ),
    ('strong', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while spoken interaction is still developing. However, Pronunciation remains less established and '
        'requires further development.'
    ),
    ('strong', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while spoken interaction meets the expected standard. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('strong', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range '
        'and also demonstrates confidence in spoken interaction. However, Pronunciation remains less '
        'established and requires further development.'
    ),
    ('strong', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and spoken '
        'interaction. However, Pronunciation remains less established and requires further development.'
    ),
    ('strong', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while pronunciation is still developing. However, Spoken interaction remains less established and '
        'requires further development.'
    ),
    ('strong', 'strong', 'developing', 'developing'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range. '
        'However, Pronunciation and spoken interaction are still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while spoken interaction meets the expected standard. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'strong', 'developing', 'confident'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range '
        'and also demonstrates confidence in spoken interaction. Pronunciation is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and spoken '
        'interaction. However, Pronunciation is still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while pronunciation meets the expected standard. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('strong', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while pronunciation meets the expected standard. Spoken interaction is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while pronunciation and spoken interaction meet the expected standard, with further scope for '
        'development.'
    ),
    ('strong', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range '
        'and also demonstrates confidence in spoken interaction. Pronunciation meets the expected standard, '
        'with further scope for development.'
    ),
    ('strong', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and spoken '
        'interaction, while pronunciation meets the expected standard, with further scope for development.'
    ),
    ('strong', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range '
        'and also demonstrates confidence in pronunciation. However, Spoken interaction remains less '
        'established and requires further development.'
    ),
    ('strong', 'strong', 'confident', 'developing'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range '
        'and also demonstrates confidence in pronunciation. Spoken interaction is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range '
        'and also demonstrates confidence in pronunciation. Spoken interaction meets the expected standard, '
        'with further scope for development.'
    ),
    ('strong', 'strong', 'confident', 'confident'): (
        '{learner_name} shows clear strengths in fluency as well as grammatical accuracy and language range, '
        'while confidence is evident in pronunciation and spoken interaction.'
    ),
    ('strong', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and spoken '
        'interaction, while confidence is evident in pronunciation.'
    ),
    ('strong', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and '
        'pronunciation. However, Spoken interaction remains less established and requires further '
        'development.'
    ),
    ('strong', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and '
        'pronunciation. However, Spoken interaction is still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and '
        'pronunciation, while spoken interaction meets the expected standard, with further scope for '
        'development.'
    ),
    ('strong', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in fluency, grammatical accuracy and language range, and '
        'pronunciation, while confidence is evident in spoken interaction.'
    ),
    ('strong', 'strong', 'strong', 'strong'): (
        'Spoken communication is a clear strength for {learner_name}, who demonstrates consistently strong '
        'performance across fluency, grammatical accuracy and language range, pronunciation, and spoken '
        'interaction.'
    ),
}
