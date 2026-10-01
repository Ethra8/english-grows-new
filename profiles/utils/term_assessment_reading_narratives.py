"""Canonical Reading performance-summary narratives for Formal Term Assessment reports.

Tuple order is always: scanning, skimming, detailed.
Each of the 125 possible rating combinations has one explicit report narrative.
"""

READING_SUBSKILL_ORDER = ("scanning", "skimming", "detailed")

READING_PERFORMANCE_NARRATIVES = {
    ('needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s reading comprehension falls well below the minimum expected "
        'standard for this level across all three assessed areas. Locating specific '
        'information, identifying main ideas and overall purpose, and understanding '
        'detailed information and meaning in context all require substantial '
        'further development.'
    ),
    ('needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'is still developing and has not yet reached the minimum expected standard '
        'for this level. The other two assessed areas, namely locating specific '
        'information and identifying main ideas and overall purpose, fall well '
        'below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the other two assessed areas, namely locating specific information and '
        'identifying main ideas and overall purpose, fall well below that standard '
        'and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is well established. However, the other two assessed areas, '
        'namely locating specific information and identifying main ideas and '
        'overall purpose, fall well below the minimum expected standard for '
        'this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong. In contrast, the other two assessed '
        'areas, namely locating specific information and identifying main ideas '
        'and overall purpose, fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'still developing and has not yet reached the minimum expected standard '
        'for this level. The other two assessed areas, namely locating specific '
        'information and understanding detailed information and meaning in '
        'context, fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'developing'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose "
        'and to understand detailed information and meaning in context are '
        'still developing and require further consolidation to reach the '
        'minimum expected standard for this level. Locating specific '
        'information falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning "
        'in context satisfactorily meets the minimum expected standard for '
        'this level, while identifying main ideas and overall purpose is '
        'still developing. However, locating specific information falls '
        'well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is well established, while identifying main ideas and '
        'overall purpose is still developing towards the minimum expected '
        'standard for this level. However, locating specific information '
        'falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying main ideas and '
        'overall purpose is still developing towards the minimum expected '
        'standard for this level. In contrast, locating specific information '
        'falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'satisfactorily meets the minimum expected standard for this level. '
        'However, the other two assessed areas, namely locating specific '
        'information and understanding detailed information and meaning '
        'in context, fall well below that standard and require '
        'substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'satisfactorily meets the minimum expected standard for this level, '
        'while understanding detailed information and meaning in context '
        'is still developing. However, locating specific information '
        'falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose "
        'and to understand detailed information and meaning in context '
        'satisfactorily meet the minimum expected standard for this level. '
        'However, locating specific information falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is well established, while identifying main ideas and '
        'overall purpose satisfactorily meets the minimum expected standard '
        'for this level. However, locating specific information falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying main ideas and '
        'overall purpose satisfactorily meets the minimum expected standard '
        'for this level. However, locating specific information falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is well established. However, the other two assessed areas, namely '
        'locating specific information and understanding detailed information '
        'and meaning in context, fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is well established, while understanding detailed information and '
        'meaning in context is still developing. However, locating specific '
        'information falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is well established, while understanding detailed information and '
        'meaning in context satisfactorily meets the minimum expected '
        'standard for this level. However, locating specific information '
        'falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'confident'): (
        "{learner_name}'s abilities to identify main ideas and overall "
        'purpose and to understand detailed information and meaning '
        'in context are well established, with confidence evident in '
        'both assessed areas. However, locating specific information '
        'falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and "
        'meaning in context is particularly strong, while identifying '
        'main ideas and overall purpose is also well established. '
        'However, locating specific information falls well below '
        'the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong. In contrast, the other two assessed areas, '
        'namely locating specific information and understanding detailed '
        'information and meaning in context, fall well below the minimum '
        'expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong, while understanding detailed information '
        'and meaning in context is still developing. However, locating '
        'specific information falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong, while understanding detailed information '
        'and meaning in context satisfactorily meets the minimum expected '
        'standard for this level. However, locating specific information '
        'falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'strong', 'confident'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong, while understanding detailed information '
        'and meaning in context is also well established. However, locating '
        'specific information falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose "
        'and to understand detailed information and meaning in context are '
        'particularly strong. However, locating specific information falls '
        'well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is still developing "
        'and has not yet reached the minimum expected standard for this level. '
        'The other two assessed areas, namely identifying main ideas and overall '
        'purpose and understanding detailed information and meaning in context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'developing'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are still developing and require '
        'further consolidation to reach the minimum expected standard for this level. '
        'Identifying main ideas and overall purpose falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level, while '
        'locating specific information is still developing. Identifying main ideas '
        'and overall purpose falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while locating specific information is still '
        'developing towards the minimum expected standard for this level. However, '
        'identifying main ideas and overall purpose falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while locating specific information is still '
        'developing towards the minimum expected standard for this level. In contrast, '
        'identifying main ideas and overall purpose falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'developing', 'needs_work'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are still developing and require further '
        'consolidation to reach the minimum expected standard for this level. '
        'Understanding detailed information and meaning in context falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'developing', 'developing'): (
        "{learner_name}'s reading comprehension is still developing across all three "
        'assessed areas. Locating specific information, identifying main ideas and '
        'overall purpose, and understanding detailed information and meaning in context '
        'have not yet reached the minimum expected standard for this level and require '
        'further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory'): (
        "{learner_name}'s understanding of detailed information and meaning in context "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'locating specific information and identifying main ideas and overall purpose '
        'are still developing and require further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established. However, locating specific information and '
        'identifying main ideas and overall purpose are still developing and require '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong. However, the other two assessed areas, namely '
        'locating specific information and identifying main ideas and overall purpose, '
        'are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'satisfactorily meets the minimum expected standard for this level, while '
        'locating specific information is still developing. Understanding detailed '
        'information and meaning in context falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'satisfactorily meets the minimum expected standard for this level. '
        'Locating specific information and understanding detailed information and '
        'meaning in context are still developing and require further consolidation '
        'to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose and "
        'to understand detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level. However, locating '
        'specific information is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while identifying main ideas and overall purpose '
        'satisfactorily meets the minimum expected standard for this level. Locating '
        'specific information is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while identifying main ideas and overall '
        'purpose satisfactorily meets the minimum expected standard for this level. '
        'Locating specific information is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is well "
        'established, while locating specific information is still developing towards '
        'the minimum expected standard for this level. Understanding detailed '
        'information and meaning in context falls well below that standard and '
        'requires substantial further development.'
    ),
    ('developing', 'confident', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is well "
        'established. However, locating specific information and understanding detailed '
        'information and meaning in context are still developing and require further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is well "
        'established, while understanding detailed information and meaning in context '
        'satisfactorily meets the minimum expected standard for this level. Locating '
        'specific information is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('developing', 'confident', 'confident'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose and to "
        'understand detailed information and meaning in context are well established, '
        'with confidence evident in both assessed areas. However, locating specific '
        'information is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while identifying main ideas and overall '
        'purpose is also well established. However, locating specific information '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while locating specific information is still developing '
        'towards the minimum expected standard for this level. Understanding detailed '
        'information and meaning in context falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'strong', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong. However, locating specific information and understanding '
        'detailed information and meaning in context are still developing and require '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for this level. '
        'Locating specific information is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'confident'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while understanding detailed information and meaning '
        'in context is also well established. However, locating specific information '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose and to "
        'understand detailed information and meaning in context are particularly strong. '
        'However, locating specific information is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to locate specific information satisfactorily meets "
        'the minimum expected standard for this level. However, the other two assessed '
        'areas, namely identifying main ideas and overall purpose and understanding '
        'detailed information and meaning in context, fall well below that standard '
        'and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s ability to locate specific information satisfactorily meets "
        'the minimum expected standard for this level, while understanding detailed '
        'information and meaning in context is still developing. However, identifying '
        'main ideas and overall purpose falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context satisfactorily meet the minimum '
        'expected standard for this level. However, identifying main ideas and overall '
        'purpose falls well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, identifying '
        'main ideas and overall purpose falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, identifying '
        'main ideas and overall purpose falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s ability to locate specific information satisfactorily meets "
        'the minimum expected standard for this level, while identifying main ideas '
        'and overall purpose is still developing. Understanding detailed information '
        'and meaning in context falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'developing', 'developing'): (
        "{learner_name}'s ability to locate specific information satisfactorily meets "
        'the minimum expected standard for this level. However, the other two assessed '
        'areas, namely identifying main ideas and overall purpose and understanding '
        'detailed information and meaning in context, are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context satisfactorily meet the minimum '
        'expected standard for this level. However, identifying main ideas and overall '
        'purpose is still developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is well established, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, identifying '
        'main ideas and overall purpose is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning in "
        'context is particularly strong, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, identifying '
        'main ideas and overall purpose is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose satisfactorily meet the minimum expected '
        'standard for this level. However, understanding detailed information and '
        'meaning in context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose satisfactorily meet the minimum expected '
        'standard for this level. However, understanding detailed information and '
        'meaning in context is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s reading comprehension satisfactorily meets the minimum "
        'expected standard across all three assessed areas. Locating specific '
        'information, identifying main ideas and overall purpose, and understanding '
        'detailed information and meaning in context are all satisfactory for this '
        'level, although there is still considerable scope for further development '
        'and consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is well established. Although locating specific information '
        'and identifying main ideas and overall purpose satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for '
        'further development and consolidation in both areas.'
    ),
    ('satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong. Although locating specific information '
        'and identifying main ideas and overall purpose satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for '
        'further development and consolidation in both areas.'
    ),
    ('satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'well established, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'well established, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is well established. Although locating specific information and '
        'understanding detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level, there is still scope '
        'for further development and consolidation in both areas.'
    ),
    ('satisfactory', 'confident', 'confident'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose "
        'and to understand detailed information and meaning in context are well '
        'established, with confidence evident in both assessed areas. Although '
        'locating specific information satisfactorily meets the minimum expected '
        'standard for this level, there is still scope for further development '
        'and consolidation in this area.'
    ),
    ('satisfactory', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while identifying main ideas and '
        'overall purpose is also well established. Although locating specific '
        'information satisfactorily meets the minimum expected standard for '
        'this level, there is still scope for further development and '
        'consolidation in this area.'
    ),
    ('satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong, while locating specific information satisfactorily '
        'meets the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong. Although locating specific information and '
        'understanding detailed information and meaning in context satisfactorily '
        'meet the minimum expected standard for this level, there is still scope '
        'for further development and consolidation in both areas.'
    ),
    ('satisfactory', 'strong', 'confident'): (
        "{learner_name}'s ability to identify main ideas and overall purpose "
        'is particularly strong, while understanding detailed information '
        'and meaning in context is also well established. Although locating '
        'specific information satisfactorily meets the minimum expected '
        'standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('satisfactory', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose "
        'and to understand detailed information and meaning in context are '
        'particularly strong. Although locating specific information '
        'satisfactorily meets the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in this area.'
    ),
    ('confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is well established. "
        'However, the other two assessed areas, namely identifying main ideas and '
        'overall purpose and understanding detailed information and meaning in '
        'context, fall well below the minimum expected standard for this level '
        'and require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing'): (
        "{learner_name}'s ability to locate specific information is well established, "
        'while understanding detailed information and meaning in context is still '
        'developing. However, identifying main ideas and overall purpose falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is well established, "
        'while understanding detailed information and meaning in context satisfactorily '
        'meets the minimum expected standard for this level. However, identifying '
        'main ideas and overall purpose falls well below that standard and '
        'requires substantial further development.'
    ),
    ('confident', 'needs_work', 'confident'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are well established, with '
        'confidence evident in both assessed areas. However, identifying main '
        'ideas and overall purpose falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while locating specific information '
        'is also well established. However, identifying main ideas and overall '
        'purpose falls well below the minimum expected standard for this level '
        'and requires substantial further development.'
    ),
    ('confident', 'developing', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is well established, "
        'while identifying main ideas and overall purpose is still developing. '
        'However, understanding detailed information and meaning in context '
        'falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('confident', 'developing', 'developing'): (
        "{learner_name}'s ability to locate specific information is well established. "
        'However, the other two assessed areas, namely identifying main ideas '
        'and overall purpose and understanding detailed information and meaning '
        'in context, are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is well established, "
        'while understanding detailed information and meaning in context satisfactorily '
        'meets the minimum expected standard for this level. Identifying main ideas '
        'and overall purpose is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('confident', 'developing', 'confident'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are well established, with '
        'confidence evident in both assessed areas. However, identifying main '
        'ideas and overall purpose is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while locating specific information '
        'is also well established. However, identifying main ideas and overall '
        'purpose is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level.'
    ),
    ('confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is well established, "
        'while identifying main ideas and overall purpose satisfactorily meets '
        'the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to locate specific information is well established, "
        'while identifying main ideas and overall purpose satisfactorily meets '
        'the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is well established. "
        'Although identifying main ideas and overall purpose and understanding '
        'detailed information and meaning in context satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for '
        'further development and consolidation in both areas.'
    ),
    ('confident', 'satisfactory', 'confident'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are well established, with '
        'confidence evident in both assessed areas. Although identifying main '
        'ideas and overall purpose satisfactorily meets the minimum expected '
        'standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('confident', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while locating specific information '
        'is also well established. Although identifying main ideas and overall '
        'purpose satisfactorily meets the minimum expected standard for this '
        'level, there is still scope for further development and '
        'consolidation in this area.'
    ),
    ('confident', 'confident', 'needs_work'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are well established, with confidence '
        'evident in both assessed areas. However, understanding detailed '
        'information and meaning in context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'developing'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are well established, with confidence '
        'evident in both assessed areas. However, understanding detailed '
        'information and meaning in context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'confident', 'satisfactory'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are well established, with confidence '
        'evident in both assessed areas. Although understanding detailed '
        'information and meaning in context satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('confident', 'confident', 'confident'): (
        "{learner_name}'s reading comprehension is well established across all "
        'three assessed areas. Locating specific information, identifying '
        'main ideas and overall purpose, and understanding detailed information '
        'and meaning in context are all handled with confidence at this level.'
    ),
    ('confident', 'confident', 'strong'): (
        "{learner_name}'s ability to understand detailed information and meaning "
        'in context is particularly strong, while locating specific information '
        'and identifying main ideas and overall purpose are also well established, '
        'with confidence evident in both areas.'
    ),
    ('confident', 'strong', 'needs_work'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while locating specific information is also well '
        'established. However, understanding detailed information and meaning '
        'in context falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('confident', 'strong', 'developing'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while locating specific information is also well '
        'established. However, understanding detailed information and meaning '
        'in context is still developing and requires further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'satisfactory'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while locating specific information is also well '
        'established. Although understanding detailed information and meaning '
        'in context satisfactorily meets the minimum expected standard for '
        'this level, there is still scope for further development and '
        'consolidation in this area.'
    ),
    ('confident', 'strong', 'confident'): (
        "{learner_name}'s ability to identify main ideas and overall purpose is "
        'particularly strong, while locating specific information and understanding '
        'detailed information and meaning in context are also well established, '
        'with confidence evident in both areas.'
    ),
    ('confident', 'strong', 'strong'): (
        "{learner_name}'s abilities to identify main ideas and overall purpose "
        'and to understand detailed information and meaning in context are '
        'particularly strong. The ability to locate specific information '
        'is also well established, with confidence evident in this area.'
    ),
    ('strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is particularly strong. "
        'However, the other two assessed areas, namely identifying main ideas and '
        'overall purpose and understanding detailed information and meaning in context, '
        'fall well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'developing'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while understanding detailed information and meaning in context is still '
        'developing. However, identifying main ideas and overall purpose falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while understanding detailed information and meaning in context satisfactorily '
        'meets the minimum expected standard for this level. However, identifying '
        'main ideas and overall purpose falls well below that standard and '
        'requires substantial further development.'
    ),
    ('strong', 'needs_work', 'confident'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while understanding detailed information and meaning in context is also '
        'well established. However, identifying main ideas and overall purpose '
        'falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'needs_work', 'strong'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are particularly strong. '
        'However, identifying main ideas and overall purpose falls well below '
        'the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'developing', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose is still developing. '
        'However, understanding detailed information and meaning in context '
        'falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'developing', 'developing'): (
        "{learner_name}'s ability to locate specific information is particularly strong. "
        'However, the other two assessed areas, namely identifying main ideas '
        'and overall purpose and understanding detailed information and meaning '
        'in context, are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while understanding detailed information and meaning in context satisfactorily '
        'meets the minimum expected standard for this level. Identifying main ideas '
        'and overall purpose is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('strong', 'developing', 'confident'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while understanding detailed information and meaning in context is also '
        'well established. However, identifying main ideas and overall purpose '
        'is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('strong', 'developing', 'strong'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are particularly strong. '
        'However, identifying main ideas and overall purpose is still developing '
        'and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose satisfactorily meets '
        'the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose satisfactorily meets '
        'the minimum expected standard for this level. However, understanding '
        'detailed information and meaning in context is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is particularly strong. "
        'Although identifying main ideas and overall purpose and understanding '
        'detailed information and meaning in context satisfactorily meet the '
        'minimum expected standard for this level, there is still scope '
        'for further development and consolidation in both areas.'
    ),
    ('strong', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while understanding detailed information and meaning in context is also '
        'well established. Although identifying main ideas and overall purpose '
        'satisfactorily meets the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in this area.'
    ),
    ('strong', 'satisfactory', 'strong'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are particularly strong. '
        'Although identifying main ideas and overall purpose satisfactorily '
        'meets the minimum expected standard for this level, there is still '
        'scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'needs_work'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose is also well established. '
        'However, understanding detailed information and meaning in context falls '
        'well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'confident', 'developing'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose is also well established. '
        'However, understanding detailed information and meaning in context '
        'is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('strong', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose is also well established. '
        'Although understanding detailed information and meaning in context '
        'satisfactorily meets the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'confident'): (
        "{learner_name}'s ability to locate specific information is particularly strong, "
        'while identifying main ideas and overall purpose and understanding '
        'detailed information and meaning in context are also well established, '
        'with confidence evident in both areas.'
    ),
    ('strong', 'confident', 'strong'): (
        "{learner_name}'s abilities to locate specific information and to understand "
        'detailed information and meaning in context are particularly strong. '
        'The ability to identify main ideas and overall purpose is also '
        'well established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'needs_work'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are particularly strong. However, '
        'understanding detailed information and meaning in context falls '
        'well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'strong', 'developing'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are particularly strong. However, '
        'understanding detailed information and meaning in context is still '
        'developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'strong', 'satisfactory'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are particularly strong. Although '
        'understanding detailed information and meaning in context satisfactorily '
        'meets the minimum expected standard for this level, there is still '
        'scope for further development and consolidation in this area.'
    ),
    ('strong', 'strong', 'confident'): (
        "{learner_name}'s abilities to locate specific information and to identify "
        'main ideas and overall purpose are particularly strong. The ability '
        'to understand detailed information and meaning in context is also '
        'well established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'strong'): (
        "{learner_name}'s reading comprehension is particularly strong across "
        'all three assessed areas. Locating specific information, identifying '
        'main ideas and overall purpose, and understanding detailed information '
        'and meaning in context are all particular strengths at this level.'
    ),
}
