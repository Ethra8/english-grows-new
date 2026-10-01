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
        "{learner_name}'s listening comprehension falls well below the minimum expected "
        'standard for this level across all three assessed areas. Understanding the main '
        'ideas and overall message, identifying specific information and key details, '
        'and understanding detailed information and meaning in context all require '
        'substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'is still developing and has not yet reached the minimum expected standard for '
        'this level. Understanding the main ideas and overall message, as well as '
        'identifying specific information and key details, falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'understanding the main ideas and overall message, as well as identifying '
        'specific information and key details, falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is well established. However, understanding the main ideas '
        'and overall message, as well as identifying specific information and '
        'key details, falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong. In contrast, understanding the main '
        'ideas and overall message, as well as identifying specific information '
        'and key details, falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details is still "
        'developing and has not yet reached the minimum expected standard for this level. '
        'Furthermore, the other two assessed areas, namely understanding the main ideas '
        'and overall message, and understanding detailed information and meaning in context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'developing'): (
        "{learner_name}'s abilities to identify specific information and key details and "
        'to understand detailed information and meaning in context are still developing '
        'and have not yet reached the minimum expected standard for this level. '
        'Understanding the main ideas and overall message falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level, while the '
        'ability to identify specific information and key details is still developing. '
        'However, understanding the main ideas and overall message falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while identifying specific information and '
        'key details is still developing towards the minimum expected standard for '
        'this level. However, understanding the main ideas and overall message falls '
        'well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying specific information '
        'and key details is still developing towards the minimum expected standard '
        'for this level. In contrast, understanding the main ideas and overall '
        'message falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'satisfactorily meets the minimum expected standard for this level. '
        'Furthermore, the other two assessed areas, namely understanding the main '
        'ideas and overall message and understanding detailed information and '
        'meaning in context, fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'satisfactorily meets the minimum expected standard for this level. '
        'Understanding detailed information and meaning in context is still '
        'developing, whereas understanding the main ideas and overall message '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard in '
        'identifying specific information and key details and understanding '
        'detailed information and meaning in context. However, understanding '
        'the main ideas and overall message falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is well established, while identifying specific information '
        'and key details satisfactorily meets the minimum expected standard for '
        'this level. However, understanding the main ideas and overall message '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying specific information '
        'and key details satisfactorily meets the minimum expected standard for '
        'this level. In contrast, understanding the main ideas and overall message '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established. However, the other two assessed areas, namely '
        'understanding the main ideas and overall message and understanding '
        'detailed information and meaning in context, fall well below the '
        'minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding detailed information and meaning '
        'in context is still developing. However, understanding the main ideas '
        'and overall message falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this '
        'level. However, understanding the main ideas and overall message falls '
        'well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'confident'): (
        "{learner_name}'s abilities to identify specific information and key "
        'details and to understand detailed information and meaning in context '
        'are well established, with confidence evident in both assessed areas. '
        'However, understanding the main ideas and overall message falls well '
        'below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying specific information '
        'and key details is also well established. However, understanding the '
        'main ideas and overall message falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong. In contrast, the other two assessed areas, '
        'namely understanding the main ideas and overall message and understanding '
        'detailed information and meaning in context, fall well below the '
        'minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding detailed information and '
        'meaning in context is still developing. However, understanding the '
        'main ideas and overall message falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding detailed information and '
        'meaning in context satisfactorily meets the minimum expected standard '
        'for this level. However, understanding the main ideas and overall '
        'message falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'confident'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding detailed information and '
        'meaning in context is also well established. However, understanding '
        'the main ideas and overall message falls well below the minimum '
        'expected standard for this level and requires substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify specific information and key "
        'details and to understand detailed information and meaning in context '
        'are particularly strong. However, understanding the main ideas and '
        'overall message falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s understanding of the main ideas and overall message is still "
        'developing and has not yet reached the minimum expected standard for this level. '
        'The other two assessed areas, namely identifying specific information and key '
        'details and understanding detailed information and meaning in context, fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'developing'): (
        "{learner_name}'s abilities to understand the main ideas and overall message and "
        'to understand detailed information and meaning in context are still developing '
        'and require further consolidation to reach the minimum expected standard for '
        'this level. Identifying specific information and key details falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level, while '
        'understanding the main ideas and overall message is still developing. '
        'Identifying specific information and key details falls well below that '
        'standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while understanding the main ideas and overall '
        'message is still developing towards the minimum expected standard for this '
        'level. However, identifying specific information and key details falls well '
        'below that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while understanding the main ideas and '
        'overall message is still developing towards the minimum expected standard '
        'for this level. In contrast, identifying specific information and key '
        'details falls well below that standard and requires substantial further '
        'development.'
    ),
    ('developing', 'developing', 'needs_work'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are still developing '
        'and require further consolidation to reach the minimum expected standard '
        'for this level. Understanding detailed information and meaning in context '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'developing'): (
        "{learner_name}'s listening comprehension is still developing across all "
        'three assessed areas. Understanding the main ideas and overall message, '
        'identifying specific information and key details, and understanding detailed '
        'information and meaning in context have not yet reached the minimum expected '
        'standard for this level and require further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'understanding the main ideas and overall message and identifying specific '
        'information and key details are still developing and require further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established. However, understanding the main ideas and '
        'overall message and identifying specific information and key details are '
        'still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong. However, the other two assessed areas, '
        'namely understanding the main ideas and overall message and identifying '
        'specific information and key details, are still developing and require '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'satisfactorily meets the minimum expected standard for this level, while '
        'understanding the main ideas and overall message is still developing. '
        'Understanding detailed information and meaning in context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'satisfactorily meets the minimum expected standard for this level. '
        'Understanding the main ideas and overall message, as well as detailed '
        'information and meaning in context, is still developing and requires '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s abilities to identify specific information and key details "
        'and to understand detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level. However, understanding '
        'the main ideas and overall message is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while identifying specific information and '
        'key details satisfactorily meets the minimum expected standard for this '
        'level. Understanding the main ideas and overall message is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while identifying specific information '
        'and key details satisfactorily meets the minimum expected standard for '
        'this level. Understanding the main ideas and overall message is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding the main ideas and overall '
        'message is still developing towards the minimum expected standard for '
        'this level. Understanding detailed information and meaning in context '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established. However, understanding the main ideas and overall '
        'message, as well as detailed information and meaning in context, is still '
        'developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this '
        'level. Understanding the main ideas and overall message is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'confident'): (
        "{learner_name}'s abilities to identify specific information and key details "
        'and to understand detailed information and meaning in context are well '
        'established, with confidence evident in both assessed areas. However, '
        'understanding the main ideas and overall message is still developing '
        'and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying specific information '
        'and key details is also well established. However, understanding the '
        'main ideas and overall message is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message is still developing towards the minimum expected standard for '
        'this level. Understanding detailed information and meaning in context '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'strong', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong. However, understanding the main ideas and overall '
        'message, as well as detailed information and meaning in context, is still '
        'developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding detailed information and '
        'meaning in context satisfactorily meets the minimum expected standard '
        'for this level. Understanding the main ideas and overall message is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'confident'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding detailed information and '
        'meaning in context is also well established. However, understanding '
        'the main ideas and overall message is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify specific information and key details "
        'and to understand detailed information and meaning in context are particularly '
        'strong. However, understanding the main ideas and overall message is still '
        'developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s understanding of the main ideas and overall message satisfactorily "
        'meets the minimum expected standard for this level. However, the other two assessed '
        'areas, namely identifying specific information and key details and understanding '
        'detailed information and meaning in context, fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s understanding of the main ideas and overall message satisfactorily "
        'meets the minimum expected standard for this level, while understanding detailed '
        'information and meaning in context is still developing. Identifying specific '
        'information and key details falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level. However, identifying '
        'specific information and key details falls well below that standard '
        'and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while understanding the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for this level. '
        'However, identifying specific information and key details falls well below '
        'that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while understanding the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for this level. '
        'In contrast, identifying specific information and key details falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s understanding of the main ideas and overall message satisfactorily "
        'meets the minimum expected standard for this level, while identifying specific '
        'information and key details is still developing. Understanding detailed '
        'information and meaning in context falls well below that standard and '
        'requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'developing'): (
        "{learner_name}'s understanding of the main ideas and overall message satisfactorily "
        'meets the minimum expected standard for this level. The other two assessed '
        'areas, namely identifying specific information and key details and understanding '
        'detailed information and meaning in context, are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level. However, identifying '
        'specific information and key details is still developing and requires '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while understanding the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for this level. '
        'Identifying specific information and key details is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while understanding the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for this level. '
        'Identifying specific information and key details is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details satisfactorily meet '
        'the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details satisfactorily meet '
        'the minimum expected standard for this level. Understanding detailed '
        'information and meaning in context is still developing and requires '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s listening comprehension satisfactorily meets the minimum "
        'expected standard across all three assessed areas. Understanding the main '
        'ideas and overall message, identifying specific information and key details, '
        'and understanding detailed information and meaning in context are all '
        'satisfactory for this level, with further scope for development and consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established. Understanding the main ideas and overall message '
        'and identifying specific information and key details satisfactorily meet '
        'the minimum expected standard for this level, with further scope for '
        'development and consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong. Understanding the main ideas and overall '
        'message and identifying specific information and key details satisfactorily '
        'meet the minimum expected standard for this level, with further scope '
        'for development and consolidation.'
    ),
    ('satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding the main ideas and overall message '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'understanding detailed information and meaning in context falls well below '
        'that standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding the main ideas and overall message '
        'satisfactorily meets the minimum expected standard for this level. '
        'Understanding detailed information and meaning in context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is well established, while understanding the main ideas and overall message '
        'and understanding detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level, with further scope '
        'for development and consolidation.'
    ),
    ('satisfactory', 'confident', 'confident'): (
        "{learner_name}'s abilities to identify specific information and key details "
        'and to understand detailed information and meaning in context are well '
        'established, with confidence evident in both assessed areas. Understanding '
        'the main ideas and overall message satisfactorily meets the minimum '
        'expected standard for this level, with further scope for development.'
    ),
    ('satisfactory', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying specific information '
        'and key details is also well established. Understanding the main ideas '
        'and overall message satisfactorily meets the minimum expected standard '
        'for this level, with further scope for development and consolidation.'
    ),
    ('satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for this level. '
        'However, understanding detailed information and meaning in context '
        'falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for this level. '
        'Understanding detailed information and meaning in context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong. Understanding the main ideas and overall message '
        'and understanding detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level, with further scope '
        'for development and consolidation.'
    ),
    ('satisfactory', 'strong', 'confident'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding detailed information and '
        'meaning in context is also well established. Understanding the main '
        'ideas and overall message satisfactorily meets the minimum expected '
        'standard for this level, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify specific information and key "
        'details and to understand detailed information and meaning in context '
        'are particularly strong. Although the ability to understand the main ideas and overall '
        'message satisfactorily meets the minimum expected standard for '
        'this level, there is still further scope for development and consolidation.'
    ),
    ('confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established. However, the other two assessed areas, namely '
        'identifying specific information and key details and understanding '
        'detailed information and meaning in context, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established, while understanding detailed information and meaning '
        'in context is still developing. However, identifying specific information '
        'and key details falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this level. '
        'However, identifying specific information and key details falls well below '
        'that standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'confident'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are well '
        'established, with confidence evident in both assessed areas. However, '
        'identifying specific information and key details falls well below the '
        'minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('confident', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while understanding the main ideas '
        'and overall message is also well established. However, identifying '
        'specific information and key details falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'developing', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established, while identifying specific information and key details '
        'is still developing. However, understanding detailed information and '
        'meaning in context falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('confident', 'developing', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established. However, the other two assessed areas, namely '
        'identifying specific information and key details and understanding '
        'detailed information and meaning in context, are still developing '
        'and require further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('confident', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this '
        'level. Identifying specific information and key details is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'confident'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are well '
        'established, with confidence evident in both assessed areas. However, '
        'identifying specific information and key details is still developing '
        'and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('confident', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while understanding the main ideas '
        'and overall message is also well established. However, identifying '
        'specific information and key details is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established, while identifying specific information and key details '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'understanding detailed information and meaning in context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established, while identifying specific information and key details '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'understanding detailed information and meaning in context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is well established. Although identifying specific information and key '
        'details and understanding detailed information and meaning in context '
        'satisfactorily meet the minimum expected standard for this level, there '
        'is still scope for further development and consolidation in both areas.'
    ),
    ('confident', 'satisfactory', 'confident'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are well '
        'established, with confidence evident in both assessed areas. Although '
        'identifying specific information and key details satisfactorily meets '
        'the minimum expected standard for this level, there is still scope '
        'for further development and consolidation in this area.'
    ),
    ('confident', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while understanding the main ideas '
        'and overall message is also well established. Although identifying '
        'specific information and key details satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('confident', 'confident', 'needs_work'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are well established, '
        'with confidence evident in both assessed areas. However, understanding '
        'detailed information and meaning in context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'developing'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are well established, '
        'with confidence evident in both assessed areas. However, understanding '
        'detailed information and meaning in context is still developing and '
        'requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('confident', 'confident', 'satisfactory'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are well established, '
        'with confidence evident in both assessed areas. Although understanding '
        'detailed information and meaning in context satisfactorily meets the '
        'minimum expected standard for this level, there is still scope for '
        'further development and consolidation in this area.'
    ),
    ('confident', 'confident', 'confident'): (
        "{learner_name}'s listening comprehension is well established across all "
        'three assessed areas. Understanding the main ideas and overall message, '
        'identifying specific information and key details, and understanding '
        'detailed information and meaning in context are all handled with '
        'confidence at this level.'
    ),
    ('confident', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while understanding the main ideas '
        'and overall message and identifying specific information and key '
        'details are also well established, with confidence evident in both areas.'
    ),
    ('confident', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message is also well established. However, understanding detailed '
        'information and meaning in context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'developing'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message is also well established. However, understanding detailed '
        'information and meaning in context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message is also well established. Although understanding detailed '
        'information and meaning in context satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('confident', 'strong', 'confident'): (
        "{learner_name}'s ability to identify specific information and key details "
        'is particularly strong, while understanding the main ideas and overall '
        'message and understanding detailed information and meaning in context '
        'are also well established, with confidence evident in both areas.'
    ),
    ('confident', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify specific information and key "
        'details and to understand detailed information and meaning in context '
        'are particularly strong. Understanding the main ideas and overall '
        'message is also well established, with confidence evident in this area.'
    ),
    ('strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong. However, the other two assessed areas, namely '
        'identifying specific information and key details and understanding '
        'detailed information and meaning in context, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('strong', 'needs_work', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while understanding detailed information and meaning '
        'in context is still developing. However, identifying specific information '
        'and key details falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this level. '
        'However, identifying specific information and key details falls well below '
        'that standard and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while understanding detailed information and meaning '
        'in context is also well established. However, identifying specific information '
        'and key details falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'strong'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are particularly '
        'strong. However, identifying specific information and key details falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'developing', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while identifying specific information and key '
        'details is still developing. However, understanding detailed information '
        'and meaning in context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong. However, the other two assessed areas, namely '
        'identifying specific information and key details and understanding '
        'detailed information and meaning in context, are still developing '
        'and require further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this '
        'level. Identifying specific information and key details is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'developing', 'confident'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while understanding detailed information and '
        'meaning in context is also well established. However, identifying '
        'specific information and key details is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'strong'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are particularly '
        'strong. However, identifying specific information and key details is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while identifying specific information and key '
        'details satisfactorily meets the minimum expected standard for this level. '
        'However, understanding detailed information and meaning in context falls '
        'well below that standard and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while identifying specific information and key '
        'details satisfactorily meets the minimum expected standard for this level. '
        'However, understanding detailed information and meaning in context is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong. Although identifying specific information and '
        'key details and understanding detailed information and meaning in context '
        'satisfactorily meet the minimum expected standard for this level, there '
        'is still scope for further development and consolidation in both areas.'
    ),
    ('strong', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while understanding detailed information and '
        'meaning in context is also well established. Although identifying '
        'specific information and key details satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('strong', 'satisfactory', 'strong'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are particularly '
        'strong. Although identifying specific information and key details satisfactorily '
        'meets the minimum expected standard for this level, there is still scope '
        'for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'needs_work'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while identifying specific information and key '
        'details is also well established. However, understanding detailed '
        'information and meaning in context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'developing'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while identifying specific information and key '
        'details is also well established. However, understanding detailed '
        'information and meaning in context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while identifying specific information and key '
        'details is also well established. Although understanding detailed '
        'information and meaning in context satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('strong', 'confident', 'confident'): (
        "{learner_name}'s ability to understand the main ideas and overall message "
        'is particularly strong, while the abilities to identify specific information '
        'and key details and to understand detailed information and meaning in '
        'context are also well established, with confidence evident in both areas.'
    ),
    ('strong', 'confident', 'strong'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to understand detailed information and meaning in context are particularly '
        'strong. The ability to identify specific information and key details is '
        'also well established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'needs_work'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are particularly strong. '
        'However, understanding detailed information and meaning in context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'strong', 'developing'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are particularly strong. '
        'However, understanding detailed information and meaning in context is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'strong', 'satisfactory'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are particularly strong. '
        'Although understanding detailed information and meaning in context satisfactorily '
        'meets the minimum expected standard for this level, there is still scope '
        'for further development and consolidation in this area.'
    ),
    ('strong', 'strong', 'confident'): (
        "{learner_name}'s abilities to understand the main ideas and overall message "
        'and to identify specific information and key details are particularly strong. '
        'The ability to understand detailed information and meaning in context is '
        'also well established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'strong'): (
        "{learner_name}'s listening comprehension is particularly strong across all "
        'three assessed areas. Understanding the main ideas and overall message, '
        'identifying specific information and key details, and understanding detailed '
        'information and meaning in context are all particular strengths at this level.'
    ),
}
