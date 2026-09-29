"""Canonical Reading performance-summary narratives for Formal Term Assessment reports.

Tuple order is always: scanning, skimming, detailed.
Each of the 125 possible rating combinations has one explicit report narrative.
"""

READING_SUBSKILL_ORDER = ("scanning", "skimming", "detailed")

READING_PERFORMANCE_NARRATIVES = {
    ('needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} is currently finding all assessed areas of reading challenging. However, with '
        'continued practice in locating specific information, identifying main ideas and overall purpose, '
        'and understanding detailed information and meaning in context, these skills can gradually become '
        'more established.'
    ),
    ('needs_work', 'needs_work', 'developing'): (
        '{learner_name} is beginning to develop the ability to understand detailed information and meaning '
        'in context. However, locating specific information and identifying main ideas and overall purpose '
        'remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in '
        'context. However, locating specific information and identifying main ideas and overall purpose '
        'remain less established and require further attention.'
    ),
    ('needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context. '
        'However, locating specific information and identifying main ideas and overall purpose remain '
        'considerably less established and would benefit from focused development.'
    ),
    ('needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context. '
        'However, locating specific information and identifying main ideas and overall purpose remain '
        'considerably less established and are the main areas requiring further development.'
    ),
    ('needs_work', 'developing', 'needs_work'): (
        '{learner_name} is beginning to develop the ability to identify main ideas and overall purpose. '
        'However, locating specific information and understanding detailed information and meaning in '
        'context remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'developing'): (
        "{learner_name}'s reading skills are still developing overall, with emerging ability in identifying "
        'main ideas and overall purpose and understanding detailed information and meaning in context. '
        'However, locating specific information remains less established and requires further attention.'
    ),
    ('needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in '
        'context, while identifying main ideas and overall purpose is still developing. However, locating '
        'specific information remains less established and requires further attention.'
    ),
    ('needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while identifying main ideas and overall purpose is still developing. However, locating specific '
        'information remains less established and would benefit from more focused practice.'
    ),
    ('needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while identifying main ideas and overall purpose is still developing. However, locating specific '
        'information remains the least established area and requires further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in identifying main ideas and overall purpose. However, '
        'locating specific information and understanding detailed information and meaning in context remain '
        'less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context is still developing. However, locating '
        'specific information remains less established and would benefit from further practice.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. However, locating specific information '
        'remains less established and is the main area requiring further development.'
    ),
    ('needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while identifying main ideas and overall purpose meets the expected standard. However, locating '
        'specific information remains less established and would benefit from focused development.'
    ),
    ('needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while identifying main ideas and overall purpose meets the expected standard. However, locating '
        'specific information remains the main area requiring further development.'
    ),
    ('needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose. However, '
        'locating specific information and understanding detailed information and meaning in context remain '
        'considerably less established and require further development.'
    ),
    ('needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context is still developing. However, locating '
        'specific information remains less established and would benefit from further practice.'
    ),
    ('needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context meets the expected standard. However, '
        'locating specific information remains less established and requires further development.'
    ),
    ('needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. However, locating specific information '
        'remains considerably less established and is the clear priority for further development.'
    ),
    ('needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context '
        'and also demonstrates confidence in identifying main ideas and overall purpose. However, locating '
        'specific information remains less established and requires further focused development.'
    ),
    ('needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose. However, '
        'locating specific information and understanding detailed information and meaning in context remain '
        'considerably less established and require further development.'
    ),
    ('needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context is still developing. However, locating '
        'specific information remains less established and requires further attention.'
    ),
    ('needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context meets the expected standard. However, '
        'locating specific information remains less established and is the main area requiring further '
        'development.'
    ),
    ('needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose and also '
        'demonstrates confidence in understanding detailed information and meaning in context. However, '
        'locating specific information remains less established and would benefit from focused development.'
    ),
    ('needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. However, locating specific information '
        'remains considerably less established and represents the main area for further development.'
    ),
    ('developing', 'needs_work', 'needs_work'): (
        '{learner_name} is beginning to develop the ability to locate specific information in a text. '
        'However, identifying main ideas and overall purpose and understanding detailed information and '
        'meaning in context remain more challenging and require further development.'
    ),
    ('developing', 'needs_work', 'developing'): (
        "{learner_name}'s reading skills are still developing overall. Some progress is evident in locating "
        'specific information in a text and understanding detailed information and meaning in context, while '
        'identifying main ideas and overall purpose remains the least established area.'
    ),
    ('developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in understanding detailed information and meaning in '
        'context. Locating specific information in a text is still developing, while identifying main ideas '
        'and overall purpose remains less established and requires further attention.'
    ),
    ('developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context. '
        'Locating specific information in a text is still developing, whereas identifying main ideas and '
        'overall purpose remains less established and would benefit from more focused development.'
    ),
    ('developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context. '
        'Locating specific information in a text is still developing, while identifying main ideas and '
        'overall purpose remains the least established area and requires further attention.'
    ),
    ('developing', 'developing', 'needs_work'): (
        "{learner_name}'s reading skills are still developing overall, with emerging ability in locating "
        'specific information in a text and identifying main ideas and overall purpose. Understanding '
        'detailed information and meaning in context remains less established and is the main area for '
        'further development.'
    ),
    ('developing', 'developing', 'developing'): (
        "{learner_name}'s reading skills are still developing across all assessed areas. Further practice "
        'in locating specific information, identifying main ideas and overall purpose, and understanding '
        'detailed information and meaning in context will help bring performance more consistently to the '
        'expected standard.'
    ),
    ('developing', 'developing', 'satisfactory'): (
        "{learner_name}'s reading skills are still developing overall, although understanding detailed "
        'information and meaning in context now meets the expected standard. Locating specific information '
        'in a text and identifying main ideas and overall purpose still require further development.'
    ),
    ('developing', 'developing', 'confident'): (
        "{learner_name}'s reading skills are still developing overall, although understanding detailed "
        'information and meaning in context is handled with confidence. Locating specific information in a '
        'text and identifying main ideas and overall purpose remain below the expected standard and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong'): (
        "{learner_name}'s reading skills are still developing overall, but understanding detailed "
        'information and meaning in context stands out as a clear strength. Locating specific information '
        'in a text and identifying main ideas and overall purpose still require further development.'
    ),
    ('developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in identifying main ideas and overall purpose. Locating '
        'specific information in a text is still developing, while understanding detailed information and '
        'meaning in context remains less established and requires more focused development.'
    ),
    ('developing', 'satisfactory', 'developing'): (
        "{learner_name}'s reading skills are still developing overall, although identifying main ideas and "
        'overall purpose meets the expected standard. Locating specific information in a text and '
        'understanding detailed information and meaning in context still require further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. Locating specific information in a text '
        'is still developing and remains the main area for further improvement.'
    ),
    ('developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while identifying main ideas and overall purpose meets the expected standard. Locating specific '
        'information in a text is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while identifying main ideas and overall purpose meets the expected standard. Locating specific '
        'information in a text is still developing and remains the main area for further improvement.'
    ),
    ('developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose. Locating '
        'specific information in a text is still developing, while understanding detailed information and '
        'meaning in context remains less established and requires further development.'
    ),
    ('developing', 'confident', 'developing'): (
        "{learner_name}'s reading skills are still developing overall, although identifying main ideas and "
        'overall purpose is handled with confidence. Locating specific information in a text and '
        'understanding detailed information and meaning in context still require further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context meets the expected standard. Locating '
        'specific information in a text is still developing and would benefit from further practice.'
    ),
    ('developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. Locating specific information in a text '
        'is still developing, however, and has not yet reached the same level of consistency.'
    ),
    ('developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context '
        'and also demonstrates confidence in identifying main ideas and overall purpose. Locating specific '
        'information in a text is still developing and remains the main area for further improvement.'
    ),
    ('developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose. Locating '
        'specific information in a text is still developing, while understanding detailed information and '
        'meaning in context remains less established and requires more focused development.'
    ),
    ('developing', 'strong', 'developing'): (
        "{learner_name}'s reading skills are still developing overall, although identifying main ideas and "
        'overall purpose stands out as a clear strength. Locating specific information in a text and '
        'understanding detailed information and meaning in context still require further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose, while '
        'understanding detailed information and meaning in context meets the expected standard. Locating '
        'specific information in a text is still developing and would benefit from further practice.'
    ),
    ('developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose and also '
        'demonstrates confidence in understanding detailed information and meaning in context. Locating '
        'specific information in a text is still developing and remains the main area for further improvement.'
    ),
    ('developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. Locating specific information in a text '
        'is still developing, however, and would benefit from further practice to bring it closer to the '
        "learner's stronger reading skills."
    ),
    ('satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in locating specific information, while identifying '
        'main ideas and overall purpose and understanding detailed information and meaning in context '
        'remain challenging and are not yet established at the expected level.'
    ),
    ('satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in locating specific information in a text. '
        'Understanding detailed information and meaning in context is still developing, while identifying '
        'main ideas and overall purpose remains less established and would benefit from further attention.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in locating specific information in a text and '
        'understanding detailed information and meaning in context. Identifying main ideas and overall '
        'purpose, however, remains less established and is the main area requiring further development.'
    ),
    ('satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while locating specific information in a text meets the expected standard. Identifying main ideas '
        'and overall purpose remains less established and would benefit from further development.'
    ),
    ('satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while locating specific information in a text meets the expected standard. Identifying main ideas '
        'and overall purpose, however, remains less established and requires further attention.'
    ),
    ('satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in locating specific information in a text. Identifying '
        'main ideas and overall purpose is still developing, while understanding detailed information and '
        'meaning in context remains less established and requires more focused development.'
    ),
    ('satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in locating specific information in a text. However, '
        'identifying main ideas and overall purpose and understanding detailed information and meaning in '
        'context are still developing and have not yet reached the same level of performance.'
    ),
    ('satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in locating specific information in a text and '
        'understanding detailed information and meaning in context. Identifying main ideas and overall '
        'purpose is still developing, however, and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in understanding detailed information and meaning in context, '
        'while locating specific information in a text meets the expected standard. Identifying main ideas '
        'and overall purpose is still developing and remains the main area for further improvement.'
    ),
    ('satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context, '
        'while locating specific information in a text meets the expected standard. Identifying main ideas '
        'and overall purpose is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in locating specific information in a text and identifying '
        'main ideas and overall purpose. Understanding detailed information and meaning in context, however, '
        'remains less established and is the main area requiring further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in locating specific information in a text and identifying '
        'main ideas and overall purpose. Understanding detailed information and meaning in context is still '
        'developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard across all assessed areas of reading. Locating specific '
        'information, identifying main ideas and overall purpose, and understanding detailed information and '
        'meaning in context are all satisfactory for this level, although there is still clear scope to '
        'develop greater consistency and depth.'
    ),
    ('satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s reading performance meets the expected standard overall, with particular confidence "
        'in understanding detailed information and meaning in context. Locating specific information in a text '
        'and identifying main ideas and overall purpose are satisfactory, with further scope for development '
        'in both areas.'
    ),
    ('satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s reading performance meets the expected standard overall. Locating specific "
        'information in a text and identifying main ideas and overall purpose are satisfactory, while '
        'understanding detailed information and meaning in context stands out as a clear strength.'
    ),
    ('satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose, while locating '
        'specific information in a text meets the expected standard. Understanding detailed information and '
        'meaning in context, however, remains less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose, while locating '
        'specific information in a text meets the expected standard. Understanding detailed information and '
        'meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s reading performance meets the expected standard overall, with particular confidence "
        'in identifying main ideas and overall purpose. Locating specific information in a text and '
        'understanding detailed information and meaning in context are satisfactory, with further scope for '
        'development in both areas.'
    ),
    ('satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying main ideas and overall purpose and in '
        'understanding detailed information and meaning in context. Locating specific information in a text '
        'also meets the expected standard, although this area is less well established by comparison.'
    ),
    ('satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context '
        'and also demonstrates confidence in identifying main ideas and overall purpose. Locating specific '
        'information in a text meets the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose, while locating '
        'specific information in a text meets the expected standard. Understanding detailed information and '
        'meaning in context, however, remains less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose, while locating '
        'specific information in a text meets the expected standard. Understanding detailed information and '
        'meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s reading performance meets the expected standard overall. Locating specific "
        'information in a text and understanding detailed information and meaning in context are satisfactory, '
        'while identifying main ideas and overall purpose stands out as a clear strength.'
    ),
    ('satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose and also '
        'demonstrates confidence in understanding detailed information and meaning in context. Locating '
        'specific information in a text meets the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong'): (
        '{learner_name} demonstrates strong reading performance in identifying main ideas and overall purpose '
        'and in understanding detailed information and meaning in context. Locating specific information in '
        'a text also meets the expected standard, although it remains the less developed of the three '
        'assessed areas.'
    ),
    ('confident', 'needs_work', 'needs_work'): (
        '{learner_name} shows confidence in locating specific information in a text. However, identifying '
        'main ideas and overall purpose and understanding detailed information and meaning in context remain '
        'considerably less established and require further development.'
    ),
    ('confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in locating specific information in a text. While '
        'understanding detailed information and meaning in context is beginning to develop, identifying '
        'main ideas and overall purpose remains less established and requires more focused attention.'
    ),
    ('confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in locating specific information in a text, while '
        'understanding detailed information and meaning in context meets the expected standard. Identifying '
        'main ideas and overall purpose, however, remains less established and is the main area requiring '
        'further development.'
    ),
    ('confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in both locating specific information in a text and '
        'understanding detailed information and meaning in context. In contrast, identifying main ideas '
        'and overall purpose remains considerably less established and would benefit from further development.'
    ),
    ('confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context '
        'and also demonstrates confidence in locating specific information in a text. Identifying main ideas '
        'and overall purpose, however, remains less established and requires further attention.'
    ),
    ('confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in locating specific information in a text. Identifying '
        'main ideas and overall purpose is still developing, while understanding detailed information and '
        'meaning in context remains less established and requires more focused development.'
    ),
    ('confident', 'developing', 'developing'): (
        '{learner_name} shows confidence in locating specific information in a text. However, identifying '
        'main ideas and overall purpose and understanding detailed information and meaning in context are '
        'still developing and have not yet reached the expected standard.'
    ),
    ('confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in locating specific information in a text, while '
        'understanding detailed information and meaning in context meets the expected standard. Identifying '
        'main ideas and overall purpose is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in locating specific information in a text and understanding '
        'detailed information and meaning in context. Identifying main ideas and overall purpose is still '
        'developing, however, and remains the main area for further improvement.'
    ),
    ('confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context '
        'and also demonstrates confidence in locating specific information in a text. Identifying main ideas '
        'and overall purpose is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in locating specific information in a text, while identifying '
        'main ideas and overall purpose meets the expected standard. Understanding detailed information and '
        'meaning in context, however, remains less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in locating specific information in a text, while identifying '
        'main ideas and overall purpose meets the expected standard. Understanding detailed information and '
        'meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard across all assessed areas of reading, with particular '
        'confidence in locating specific information in a text. Identifying main ideas and overall purpose '
        'and understanding detailed information and meaning in context are satisfactory, with further scope '
        'for development in both areas.'
    ),
    ('confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in locating specific information in a text and understanding '
        'detailed information and meaning in context. Identifying main ideas and overall purpose also meets '
        'the expected standard, although this area is less well established by comparison.'
    ),
    ('confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in understanding detailed information and meaning in context '
        'and also demonstrates confidence in locating specific information in a text. Identifying main ideas '
        'and overall purpose meets the expected standard, with further scope for development.'
    ),
    ('confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in locating specific information in a text and identifying '
        'main ideas and overall purpose. Understanding detailed information and meaning in context, however, '
        'remains considerably less established and is the main area requiring further development.'
    ),
    ('confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in locating specific information in a text and identifying '
        'main ideas and overall purpose. By contrast, understanding detailed information and meaning in '
        'context is still developing and has not yet reached the same level of performance.'
    ),
    ('confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in locating specific information in a text and identifying '
        'main ideas and overall purpose. Understanding detailed information and meaning in context also meets '
        'the expected standard, although there is still scope to develop greater depth and consistency in '
        'this area.'
    ),
    ('confident', 'confident', 'confident'): (
        '{learner_name} reads with confidence across all assessed areas. This is evident in the ability to '
        'locate specific information, identify main ideas and overall purpose, and understand detailed '
        'information and meaning in context.'
    ),
    ('confident', 'confident', 'strong'): (
        '{learner_name} demonstrates confident reading across all assessed areas, with understanding detailed '
        'information and meaning in context standing out as a particular strength. Confidence is also evident '
        'in locating specific information in a text and identifying main ideas and overall purpose.'
    ),
    ('confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose and also '
        'demonstrates confidence in locating specific information in a text. Understanding detailed '
        'information and meaning in context, however, remains less established and requires further development.'
    ),
    ('confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose and also '
        'demonstrates confidence in locating specific information in a text. Understanding detailed '
        'information and meaning in context is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in identifying main ideas and overall purpose and demonstrates '
        'confidence in locating specific information in a text. Understanding detailed information and '
        'meaning in context also meets the expected standard, although there remains scope for further '
        'development in this area.'
    ),
    ('confident', 'strong', 'confident'): (
        '{learner_name} demonstrates confident reading across all assessed areas, with identifying main ideas '
        'and overall purpose standing out as a clear strength. Confidence is also evident in locating specific '
        'information in a text and understanding detailed information and meaning in context.'
    ),
    ('confident', 'strong', 'strong'): (
        '{learner_name} demonstrates strong reading ability overall, with clear strengths in identifying main '
        'ideas and overall purpose and understanding detailed information and meaning in context. The learner '
        'also shows confidence in locating specific information in a text, resulting in consistently effective '
        'performance across the three assessed areas.'
    ),
    ('strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in locating specific information in a text. '
        'By contrast, identifying main ideas and overall purpose and understanding detailed '
        'information and meaning in context remain considerably less established and would '
        'benefit from further development.'
    ),
    ('strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in locating specific information in a text. '
        'Although understanding detailed information and meaning in context is beginning to '
        'develop, identifying main ideas and overall purpose remains less established and '
        'requires further attention.'
    ),
    ('strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in locating specific information in a text, '
        'while understanding detailed information and meaning in context meets the expected '
        'standard. Identifying main ideas and overall purpose, however, remains less established '
        'and is the main area requiring further development.'
    ),
    ('strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in locating specific information in a text and '
        'also demonstrates confidence in understanding detailed information and meaning in '
        'context. Identifying main ideas and overall purpose, however, remains less established '
        'and would benefit from further development.'
    ),
    ('strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in locating specific information in a text and '
        'understanding detailed information and meaning in context. In contrast, identifying '
        'main ideas and overall purpose remains considerably less established and represents '
        'the main area for development.'
    ),
    ('strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in locating specific information in a text. '
        'Identifying main ideas and overall purpose is still developing, while understanding '
        'detailed information and meaning in context remains less established and requires '
        'more focused development.'
    ),
    ('strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in locating specific information in a text. '
        'However, identifying main ideas and overall purpose and understanding detailed '
        'information and meaning in context are still developing and have not yet reached '
        'the expected standard.'
    ),
    ('strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in locating specific information in a text, '
        'while understanding detailed information and meaning in context meets the expected '
        'standard. Identifying main ideas and overall purpose is still developing and would '
        'benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in locating specific information in a text and '
        'also demonstrates confidence in understanding detailed information and meaning in '
        'context. Identifying main ideas and overall purpose is still developing and remains '
        'the main area for further improvement.'
    ),
    ('strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in locating specific information in a text and '
        'understanding detailed information and meaning in context. However, identifying main '
        'ideas and overall purpose is still developing, creating a noticeable contrast with '
        'the learner’s stronger reading skills.'
    ),
    ('strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in locating specific information in a text, '
        'while identifying main ideas and overall purpose meets the expected standard. '
        'Understanding detailed information and meaning in context, however, remains less '
        'established and requires further development.'
    ),
    ('strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in locating specific information in a text, '
        'while identifying main ideas and overall purpose meets the expected standard. '
        'Understanding detailed information and meaning in context is still developing and '
        'would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in identifying main ideas and overall '
        'purpose and understanding detailed information and meaning in context, while locating '
        'specific information in a text stands out as a clear strength.'
    ),
    ('strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in locating specific information in a text and '
        'also demonstrates confidence in understanding detailed information and meaning in '
        'context. Identifying main ideas and overall purpose meets the expected standard, '
        'although there is still scope for further development in this area.'
    ),
    ('strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in locating specific information in a text and '
        'understanding detailed information and meaning in context. Identifying main ideas and '
        'overall purpose also meets the expected standard, resulting in a positive overall '
        'reading profile with particular strengths at both detailed and specific-information level.'
    ),
    ('strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in locating specific information in a text and '
        'also demonstrates confidence in identifying main ideas and overall purpose. However, '
        'understanding detailed information and meaning in context remains less established '
        'and would benefit from further focused development.'
    ),    
    ('strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in locating specific information in a text and '
        'also demonstrates confidence in identifying main ideas and overall purpose. However, '
        'understanding detailed information and meaning in context is still developing and '
        'would benefit from further consolidation.'
    ),    
    ('strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in locating specific information in a text and '
        'also demonstrates confidence in identifying main ideas and overall purpose. At the same '
        'time, understanding detailed information and meaning in context meets the expected '
        'standard, although there is still room to develop greater depth and consistency.'
    ),    
    ('strong', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in identifying main ideas and '
        'overall purpose of a text, while understanding detailed information and meaning in context as well.' 
        "Furthermore, {learner_name}'s ability to locate specific information stands out as a clear strength."
    ),
    ('strong', 'confident', 'strong'): (
        '{learner_name} demonstrates strong reading ability overall. Identifying '
        'main ideas and overall purpose is handled with confidence, '
        'with clear strengths in locating specific information, while understanding detailed information and meaning in context.'
    ),
    ('strong', 'strong', 'needs_work'): (
        "{learner_name} shows clear strengths in locating specific information and identifying main ideas "
        "and overall purpose, but understanding detailed information and meaning in context remains "
        "considerably less established by comparison, well below this level's minimum requirements."
    ),
    ('strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in locating specific information and identifying main ideas '
        'and overall purpose. However, understanding detailed information and meaning in context is still '
        'developing, creating a noticeable contrast in current reading performance.'
    ),
    ('strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in locating specific information and identifying main ideas '
        'and overall purpose, while understanding detailed information and meaning in context meets the '
        'minimum required standard for this level and remains the less secure area by comparison.'
    ),
    ('strong', 'strong', 'confident'): (
        '{learner_name} demonstrates strong reading ability overall. Understanding detailed '
        'information and meaning in context is handled with confidence, with clear strengths in locating '
        'specific information and identifying main ideas and overall purpose.'
    ),
    ('strong', 'strong', 'strong'): (
        '{learner_name} demonstrates strong reading ability across all assessed areas, with clear '
        'strengths in locating specific information, identifying main ideas and overall purpose, and '
        'understanding detailed information and meaning in context.'
    ),
}
