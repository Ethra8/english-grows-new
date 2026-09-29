"""Canonical Listening performance-summary narratives for Formal Term Assessment reports.

Tuple order is always: gist, specific_information, detailed.
Each of the 125 possible rating combinations has one explicit report narrative.
"""

LISTENING_SUBSKILL_ORDER = (
    "gist",
    "specific_information",
    "detailed",
)

LISTENING_PERFORMANCE_NARRATIVES = {
    ('needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} is currently finding listening challenging across all three assessed areas. '
        'Understanding the main idea and overall message, identifying specific information and key details, '
        'and understanding detailed information and meaning in context all require further development to '
        'reach the expected standard.'
    ),
    ('needs_work', 'needs_work', 'developing'): (
        '{learner_name} is beginning to develop greater understanding of detailed information and meaning in '
        'context. However, understanding the main idea and overall message and identifying specific information '
        'and key details remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in context. '
        'However, understanding the main idea and overall message and identifying specific information and key '
        'details remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context. '
        'However, understanding the main idea and overall message and identifying specific information and key '
        'details remain considerably less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context. '
        'By contrast, understanding the main idea and overall message and identifying specific information and '
        'key details remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'needs_work'): (
        '{learner_name} is developing greater ability to identify specific information and key details. However, '
        'understanding the main idea and overall message and understanding detailed information and meaning in '
        'context remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'developing'): (
        '{learner_name} is developing greater ability to identify specific information and key details and to '
        'understand detailed information and meaning in context. However, understanding the main idea and overall '
        'message remains less established and is the main area requiring further development.'
    ),
    ('needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in context, '
        'while the ability to identify specific information and key details is still developing. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while the ability to identify specific information and key details is still developing. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context. '
        'The ability to identify specific information and key details is still developing, while understanding '
        'the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in identifying specific information and key details. However, '
        'understanding the main idea and overall message and understanding detailed information and meaning in '
        'context remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in identifying specific information and key details, while '
        'understanding detailed information and meaning in context is still developing. However, understanding '
        'the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. However, understanding the main idea and '
        'overall message remains less established and is the main area requiring further development.'
    ),
    ('needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while identifying specific information and key details meets the expected standard. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while identifying specific information and key details meets the expected standard. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details. However, '
        'understanding the main idea and overall message and understanding detailed information and meaning in '
        'context remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details, while '
        'understanding detailed information and meaning in context is still developing. However, understanding '
        'the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details, while '
        'understanding detailed information and meaning in context meets the expected standard. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. However, understanding the main idea and '
        'overall message remains less established and is the main area requiring further development.'
    ),
    ('needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context and '
        'also demonstrates confidence in identifying specific information and key details. However, understanding '
        'the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying specific information and key details. However, '
        'understanding the main idea and overall message and understanding detailed information and meaning in '
        'context remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying specific information and key details, while '
        'understanding detailed information and meaning in context is still developing. However, understanding '
        'the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in identifying specific information and key details, while '
        'understanding detailed information and meaning in context meets the expected standard. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in identifying specific information and key details and also '
        'demonstrates confidence in understanding detailed information and meaning in context. However, '
        'understanding the main idea and overall message remains less established and requires further development.'
    ),
    ('needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. However, understanding the main idea and '
        'overall message remains less established and is the main area requiring further development.'
    ),
    ('developing', 'needs_work', 'needs_work'): (
        '{learner_name} is beginning to develop greater understanding of the main idea and overall message. '
        'However, identifying specific information and key details and understanding detailed information and '
        'meaning in context remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'developing'): (
        '{learner_name} is developing greater ability to understand both the main idea and overall message and '
        'detailed information and meaning in context. However, identifying specific information and key details '
        'remains less established and is the main area requiring further development.'
    ),
    ('developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in context, '
        'while understanding the main idea and overall message is still developing. However, identifying specific '
        'information and key details remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while understanding the main idea and overall message is still developing. However, identifying specific '
        'information and key details remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context. '
        'Understanding the main idea and overall message is still developing, while identifying specific '
        'information and key details remains less established and requires further development.'
    ),
    ('developing', 'developing', 'needs_work'): (
        '{learner_name} is developing greater ability to understand the main idea and overall message and to '
        'identify specific information and key details. However, understanding detailed information and meaning '
        'in context remains less established and is the main area requiring further development.'
    ),
    ('developing', 'developing', 'developing'): (
        "{learner_name}'s listening skills are still developing across all three assessed areas. Understanding "
        'the main idea and overall message, identifying specific information and key details, and understanding '
        'detailed information and meaning in context all require further consolidation to reach the expected '
        'standard more consistently.'
    ),
    ('developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in context. '
        'However, understanding the main idea and overall message and identifying specific information and key '
        'details are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context. '
        'However, understanding the main idea and overall message and identifying specific information and key '
        'details are still developing and require further consolidation.'
    ),
    ('developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context. '
        'However, understanding the main idea and overall message and identifying specific information and key '
        'details are still developing and require further consolidation.'
    ),
    ('developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in identifying specific information and key details, while '
        'understanding the main idea and overall message is still developing. However, understanding detailed '
        'information and meaning in context remains less established and requires further development.'
    ),
    ('developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in identifying specific information and key details. '
        'Understanding the main idea and overall message and understanding detailed information and meaning in '
        'context are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. Understanding the main idea and overall '
        'message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while identifying specific information and key details meets the expected standard. Understanding the '
        'main idea and overall message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while identifying specific information and key details meets the expected standard. Understanding the '
        'main idea and overall message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details, while '
        'understanding the main idea and overall message is still developing. However, understanding detailed '
        'information and meaning in context remains less established and requires further development.'
    ),
    ('developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details. '
        'Understanding the main idea and overall message and understanding detailed information and meaning in '
        'context are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details, while '
        'understanding detailed information and meaning in context meets the expected standard. Understanding '
        'the main idea and overall message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. However, understanding the main idea and '
        'overall message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context and '
        'also demonstrates confidence in identifying specific information and key details. However, understanding '
        'the main idea and overall message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying specific information and key details, while '
        'understanding the main idea and overall message is still developing. However, understanding detailed '
        'information and meaning in context remains less established and requires further development.'
    ),
    ('developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying specific information and key details. '
        'Understanding the main idea and overall message and understanding detailed information and meaning in '
        'context are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in identifying specific information and key details, while '
        'understanding detailed information and meaning in context meets the expected standard. Understanding '
        'the main idea and overall message is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in identifying specific information and key details and also '
        'demonstrates confidence in understanding detailed information and meaning in context. However, '
        'understanding the main idea and overall message is still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. However, understanding the main idea and '
        'overall message is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message. '
        'However, identifying specific information and key details and understanding detailed information and '
        'meaning in context remain less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message, while '
        'understanding detailed information and meaning in context is still developing. However, identifying '
        'specific information and key details remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding both the main idea and overall message and '
        'detailed information and meaning in context. However, identifying specific information and key details '
        'remains less established and is the main area requiring further development.'
    ),
    ('satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while understanding the main idea and overall message meets the expected standard. However, identifying '
        'specific information and key details remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while understanding the main idea and overall message meets the expected standard. However, identifying '
        'specific information and key details remains less established and requires further development.'
    ),
    ('satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message, while '
        'the ability to identify specific information and key details is still developing. However, understanding '
        'detailed information and meaning in context remains less established and requires further development.'
    ),
    ('satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message. '
        'Identifying specific information and key details and understanding detailed information and meaning in '
        'context are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. Identifying specific information and key '
        'details is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while understanding the main idea and overall message meets the expected standard. Identifying specific '
        'information and key details is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while understanding the main idea and overall message meets the expected standard. Identifying specific '
        'information and key details is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message and in '
        'identifying specific information and key details. However, understanding detailed information and meaning '
        'in context remains less established and is the main area requiring further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in understanding the main idea and overall message and in '
        'identifying specific information and key details, while understanding detailed information and meaning '
        'in context is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s listening performance meets the expected standard across all three assessed areas. "
        'Understanding the main idea and overall message, identifying specific information and key details, and '
        'understanding detailed information and meaning in context are all satisfactory for this level, although '
        'there remains clear scope to develop greater consistency and depth of comprehension.'
    ),
    ('satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s listening performance meets the expected standard overall, with particular confidence "
        'in understanding detailed information and meaning in context. Understanding the main idea and overall '
        'message and identifying specific information and key details are satisfactory, with further scope for '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s listening performance meets the expected standard overall. Understanding the main idea "
        'and overall message and identifying specific information and key details are satisfactory, while '
        'understanding detailed information and meaning in context stands out as a clear strength.'
    ),
    ('satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details, while '
        'understanding the main idea and overall message meets the expected standard. However, understanding '
        'detailed information and meaning in context remains less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details, while '
        'understanding the main idea and overall message meets the expected standard. Understanding detailed '
        'information and meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s listening performance meets the expected standard overall, with particular confidence "
        'in identifying specific information and key details. Understanding the main idea and overall message and '
        'understanding detailed information and meaning in context are satisfactory, with further scope for '
        'development.'
    ),
    ('satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. Understanding the main idea and overall '
        'message also meets the expected standard, although there is still scope for further development.'
    ),
    ('satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context and '
        'also demonstrates confidence in identifying specific information and key details. Understanding the '
        'main idea and overall message meets the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying specific information and key details, while '
        'understanding the main idea and overall message meets the expected standard. However, understanding '
        'detailed information and meaning in context remains less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying specific information and key details, while '
        'understanding the main idea and overall message meets the expected standard. Understanding detailed '
        'information and meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s listening performance meets the expected standard overall. Understanding the main idea "
        'and overall message and understanding detailed information and meaning in context are satisfactory, '
        'while identifying specific information and key details stands out as a clear strength.'
    ),
    ('satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in identifying specific information and key details and also '
        'demonstrates confidence in understanding detailed information and meaning in context. Understanding the '
        'main idea and overall message meets the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. Understanding the main idea and overall '
        'message meets the expected standard, although there is still scope for further development.'
    ),
    ('confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message. However, '
        'identifying specific information and key details and understanding detailed information and meaning in '
        'context remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message, while '
        'understanding detailed information and meaning in context is still developing. However, identifying '
        'specific information and key details remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message, while '
        'understanding detailed information and meaning in context meets the expected standard. However, '
        'identifying specific information and key details remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. However, identifying specific information '
        'and key details remains less established and is the main area requiring further development.'
    ),
    ('confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context and '
        'also demonstrates confidence in understanding the main idea and overall message. However, identifying '
        'specific information and key details remains less established and requires further development.'
    ),
    ('confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message, while the '
        'ability to identify specific information and key details is still developing. However, understanding '
        'detailed information and meaning in context remains less established and requires further development.'
    ),
    ('confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message. Identifying '
        'specific information and key details and understanding detailed information and meaning in context are '
        'still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message, while '
        'understanding detailed information and meaning in context meets the expected standard. Identifying '
        'specific information and key details is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. However, identifying specific information '
        'and key details is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context and '
        'also demonstrates confidence in understanding the main idea and overall message. Identifying specific '
        'information and key details is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message, while '
        'identifying specific information and key details meets the expected standard. However, understanding '
        'detailed information and meaning in context remains less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message, while '
        'identifying specific information and key details meets the expected standard. Understanding detailed '
        'information and meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s listening performance meets the expected standard overall, with particular confidence "
        'in understanding the main idea and overall message. Identifying specific information and key details '
        'and understanding detailed information and meaning in context are satisfactory, with further scope for '
        'development.'
    ),
    ('confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. Identifying specific information and key '
        'details also meets the expected standard, although there is still scope for further development.'
    ),
    ('confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context and '
        'also demonstrates confidence in understanding the main idea and overall message. Identifying specific '
        'information and key details meets the expected standard, with further scope for development.'
    ),
    ('confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message and in '
        'identifying specific information and key details. However, understanding detailed information and '
        'meaning in context remains less established and is the main area requiring further development.'
    ),
    ('confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message and in '
        'identifying specific information and key details. However, understanding detailed information and '
        'meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in understanding the main idea and overall message and in '
        'identifying specific information and key details, while understanding detailed information and meaning '
        'in context meets the expected standard, with further scope for development.'
    ),
    ('confident', 'confident', 'confident'): (
        '{learner_name} listens with confidence across all three assessed areas. Understanding the main idea and '
        'overall message, identifying specific information and key details, and understanding detailed '
        'information and meaning in context are all handled securely and consistently.'
    ),
    ('confident', 'confident', 'strong'): (
        '{learner_name} demonstrates confident listening overall, with a clear strength in understanding detailed '
        'information and meaning in context. Confidence is also evident in understanding the main idea and overall '
        'message and in identifying specific information and key details.'
    ),
    ('confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying specific information and key details and also '
        'demonstrates confidence in understanding the main idea and overall message. However, understanding '
        'detailed information and meaning in context remains less established and requires further development.'
    ),
    ('confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying specific information and key details and also '
        'demonstrates confidence in understanding the main idea and overall message. Understanding detailed '
        'information and meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in identifying specific information and key details and also '
        'demonstrates confidence in understanding the main idea and overall message. Understanding detailed '
        'information and meaning in context meets the expected standard, with further scope for development.'
    ),
    ('confident', 'strong', 'confident'): (
        '{learner_name} demonstrates confident listening overall, with a clear strength in identifying specific '
        'information and key details. Confidence is also evident in understanding the main idea and overall '
        'message and in understanding detailed information and meaning in context.'
    ),
    ('confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in identifying specific information and key details and in '
        'understanding detailed information and meaning in context. Understanding the main idea and overall '
        'message is also handled with confidence.'
    ),
    ('strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in the ability to understand the main idea and overall message. '
        'However, the skills needed to identify specific information and key details and to understand detailed '
        'information and meaning in context remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in the ability to understand the main idea and overall message. '
        'The ability to understand detailed information and meaning in context is developing, while identifying '
        'specific information and key details remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message, while the '
        'ability to understand detailed information and meaning in context meets the expected standard. However, '
        'identifying specific information and key details remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message and also '
        'demonstrates confidence in the ability to understand detailed information and meaning in context. '
        'However, identifying specific information and key details remains less established and requires further '
        'development.'
    ),
    ('strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. However, the ability to identify specific '
        'information and key details remains less established and is the main area requiring further development.'
    ),
    ('strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message. The ability to '
        'identify specific information and key details is still developing; however, understanding detailed '
        'information and meaning in context remains less established and requires further development.'
    ),
    ('strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message. By contrast, '
        'the ability to identify specific information and key details and to understand detailed information and '
        'meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message, while '
        'understanding detailed information and meaning in context meets the expected standard. The ability to '
        'identify specific information and key details is still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message and also '
        'demonstrates confidence in understanding detailed information and meaning in context. The ability to '
        'identify specific information and key details is still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. However, the ability to identify specific '
        'information and key details is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message, while the '
        'ability to identify specific information and key details meets the expected standard. However, '
        'understanding detailed information and meaning in context remains less established and requires further '
        'development.'
    ),
    ('strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message, while the '
        'ability to identify specific information and key details meets the expected standard. Understanding '
        'detailed information and meaning in context is still developing and would benefit from further '
        'consolidation.'
    ),
    ('strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s listening performance meets the expected standard overall, with a clear strength in "
        'understanding the main idea and overall message. The ability to identify specific information and key '
        'details and to understand detailed information and meaning in context is satisfactory for this level, '
        'with further scope for development.'
    ),
    ('strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message and also '
        'demonstrates confidence in understanding detailed information and meaning in context. The ability to '
        'identify specific information and key details meets the expected standard, with further scope for '
        'development.'
    ),
    ('strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. The ability to identify specific information '
        'and key details meets the expected standard, although there is still scope for further development.'
    ),
    ('strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message and also '
        'demonstrates confidence in identifying specific information and key details. However, the ability to '
        'understand detailed information and meaning in context remains less established and requires further '
        'development.'
    ),
    ('strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message and also '
        'demonstrates confidence in identifying specific information and key details. However, the ability to '
        'understand detailed information and meaning in context is still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in understanding the main idea and overall message and also '
        'demonstrates confidence in identifying specific information and key details. Understanding detailed '
        'information and meaning in context meets the expected standard, with further scope for development.'
    ),
    ('strong', 'confident', 'confident'): (
        '{learner_name} demonstrates confident listening overall, with a clear strength in understanding the main '
        'idea and overall message. Confidence is also evident in the ability to identify specific information and '
        'key details and to understand detailed information and meaning in context.'
    ),
    ('strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'understanding detailed information and meaning in context. The ability to identify specific information '
        'and key details is also handled with confidence.'
    ),
    ('strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'identifying specific information and key details. However, the ability to understand detailed '
        'information and meaning in context remains less established and is the main area requiring further '
        'development.'
    ),
    ('strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'identifying specific information and key details. However, the ability to understand detailed '
        'information and meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'identifying specific information and key details. Understanding detailed information and meaning in '
        'context meets the expected standard, with further scope for development.'
    ),
    ('strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in understanding the main idea and overall message and in '
        'identifying specific information and key details, while the ability to understand detailed information '
        'and meaning in context is also handled with confidence.'
    ),
    ('strong', 'strong', 'strong'): (
        '{learner_name} demonstrates strong listening ability across all three assessed areas. Clear strengths '
        'are evident in understanding the main idea and overall message, identifying specific information and '
        'key details, and understanding detailed information and meaning in context.'
    ),
}
