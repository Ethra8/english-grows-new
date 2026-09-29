"""Canonical Writing performance-summary narratives for Formal Term Assessment reports.

Tuple order is always: organization, cohesion, vocabulary_grammar, register.
Each of the 625 possible rating combinations has one explicit report narrative.
"""

WRITING_SUBSKILL_ORDER = (
    "organization",
    "cohesion",
    "vocabulary_grammar",
    "register",
)

WRITING_PERFORMANCE_NARRATIVES = {
    ('needs_work', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} is currently finding written communication challenging across all four assessed areas. '
        'The organisation and clear presentation of ideas, the ability to connect ideas coherently, grammatical '
        'accuracy and language range, and the appropriate use of tone and style all require further development '
        'to reach the expected standard.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} is beginning to develop greater awareness of how tone and style should be adapted to '
        'purpose, audience and context. However, the organisation of written work, the coherent connection of '
        'ideas, and control of grammar and language range remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates satisfactory control of register and is able to adapt tone and style to '
        'purpose, audience and context at the expected level. However, the organisation of written work, cohesion, '
        'and grammatical accuracy and language range remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context. However, the ability to organise written work clearly, connect ideas coherently, and use grammar '
        'and vocabulary accurately and flexibly remains less established and requires further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. By contrast, the organisation and cohesion of written work and control of grammar and language '
        'range remain less established and require further development.'
    ),

    ('needs_work', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} is developing greater control of grammar and a broader range of vocabulary and sentence '
        'structures. However, the organisation of written work, the coherent connection of ideas, and the ability '
        'to adapt tone and style appropriately remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'developing'): (
        '{learner_name} is developing greater control of grammar and language range, while awareness of '
        'appropriate tone and style is also beginning to develop. However, the organisation of written work and '
        'the ability to connect ideas coherently remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context, '
        'while grammatical accuracy and language range are still developing. However, the organisation of written '
        'work and the coherent connection of ideas remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range are still developing. However, the organisation '
        'of written work and the ability to connect ideas coherently remain less established and require further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. Control of grammar and language range is still developing; however, the organisation and '
        'cohesion of written work remain less established and require further development.'
    ),

    ('needs_work', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range. However, the '
        'organisation of written work, the ability to connect ideas coherently, and control of register remain '
        'less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while the ability '
        'to adapt tone and style appropriately is still developing. However, the organisation and cohesion of '
        'written work remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range and in adapting '
        'tone and style appropriately to purpose, audience and context. However, the organisation of written work '
        'and the coherent connection of ideas remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. However, the '
        'organisation and cohesion of written work remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. However, the '
        'organisation and cohesion of written work remain less established and require further development.'
    ),

    ('needs_work', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in using grammar accurately and drawing on a varied range of '
        'vocabulary and sentence structures. However, the organisation of written work, the coherent connection '
        'of ideas, and the ability to adapt tone and style appropriately remain less established and require '
        'further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while control of '
        'register is still developing. However, the organisation of written work and the ability to connect ideas '
        'coherently remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while the ability to '
        'adapt tone and style appropriately meets the expected standard. However, the organisation and cohesion '
        'of written work remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context. However, the organisation and cohesion of '
        'written work remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. However, the '
        'organisation of written work and the ability to connect ideas coherently remain less established and '
        'require further development.'
    ),

    ('needs_work', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and the use of a varied range of vocabulary '
        'and sentence structures. However, the organisation of written work, the coherent connection of ideas, '
        'and the ability to adapt tone and style appropriately remain less established and require further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while control of '
        'register is still developing. However, the organisation and cohesion of written work remain less '
        'established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while the ability to '
        'adapt tone and style appropriately meets the expected standard. However, the organisation and cohesion '
        'of written work remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. However, the '
        'organisation and cohesion of written work remain less established and require further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. However, the organisation of written work and the '
        'ability to connect ideas coherently remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} is developing greater ability to connect ideas logically and maintain coherence. '
        'However, the organisation and clear presentation of written work, grammatical accuracy and language '
        'range, and the ability to adapt tone and style appropriately remain less established and require '
        'further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'developing'): (
        '{learner_name} is developing greater control of cohesion and is also beginning to adapt tone and style '
        'more appropriately to purpose, audience and context. However, the organisation of written work and '
        'control of grammar and language range remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context, '
        'while the ability to connect ideas logically and maintain coherence is still developing. However, the '
        'organisation of written work and control of grammar and language range remain less established and '
        'require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion is still developing. However, the organisation of written work and grammatical '
        'accuracy and language range remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. The ability to connect ideas logically and maintain coherence is still developing; however, '
        'the organisation of written work and control of grammar and language range remain less established and '
        'require further development.'
    ),

    ('needs_work', 'developing', 'developing', 'needs_work'): (
        '{learner_name} is developing greater control of cohesion and of grammar and language range. However, the '
        'organisation and clear presentation of written work and the ability to adapt tone and style appropriately '
        'remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'developing', 'developing'): (
        '{learner_name} is making progress in connecting ideas coherently, developing grammatical accuracy and '
        'language range, and adapting tone and style to purpose, audience and context. However, the organisation '
        'and clear presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context, '
        'while cohesion and grammatical accuracy and language range are still developing. However, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context. Cohesion and grammatical accuracy and language range are still developing, while the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. Cohesion and grammatical accuracy and language range are still developing; however, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),

    ('needs_work', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while the ability '
        'to connect ideas logically and maintain coherence is still developing. However, the organisation of '
        'written work and control of register remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range. Cohesion and the '
        'ability to adapt tone and style appropriately are still developing, while the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range and in adapting '
        'tone and style appropriately to purpose, audience and context. Cohesion is still developing; however, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. The ability to '
        'connect ideas logically and maintain coherence is still developing. However, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. Cohesion is still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),

    ('needs_work', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while the ability to '
        'connect ideas logically and maintain coherence is still developing. However, the organisation of '
        'written work and control of register remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range. Cohesion and control '
        'of register are still developing, while the organisation and clear presentation of written work remain '
        'less established and require further development.'
    ),
    ('needs_work', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while control of '
        'register meets the expected standard. The ability to connect ideas logically and maintain coherence is '
        'still developing. However, the organisation and clear presentation of written work remain less '
        'established and require further development.'
    ),
    ('needs_work', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context. Cohesion is still developing; however, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. The ability to '
        'connect ideas logically and maintain coherence is still developing. However, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),

    ('needs_work', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while the ability to '
        'connect ideas logically and maintain coherence is still developing. However, the organisation of '
        'written work and control of register remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range. Cohesion and control '
        'of register are still developing, while the organisation and clear presentation of written work remain '
        'less established and require further development.'
    ),
    ('needs_work', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while control of '
        'register meets the expected standard. Cohesion is still developing; however, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Cohesion is still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. The ability to connect ideas logically and '
        'maintain coherence is still developing. However, the organisation and clear presentation of written '
        'work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in connecting ideas logically and maintaining coherence. '
        'However, the organisation and clear presentation of written work, grammatical accuracy and language '
        'range, and control of register remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in connecting ideas logically and maintaining coherence, '
        'while the ability to adapt tone and style appropriately is still developing. However, the organisation '
        'of written work and control of grammar and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in both cohesion and the use of an appropriate register. '
        'However, the organisation and clear presentation of written work and control of grammar and language '
        'range remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while the ability to connect ideas logically and maintain coherence meets the expected standard. '
        'However, the organisation of written work and control of grammar and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. However, the organisation of written work and '
        'grammatical accuracy and language range remain less established and require further development.'
    ),

    ('needs_work', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in connecting ideas logically and maintaining coherence, '
        'while grammatical accuracy and language range are still developing. However, the organisation of '
        'written work and control of register remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in cohesion. Grammatical accuracy and language range and the '
        'ability to adapt tone and style appropriately are still developing, while the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in connecting ideas coherently and in adapting tone and style '
        'appropriately to purpose, audience and context. Grammatical accuracy and language range are still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. Grammatical accuracy and language range are still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. Grammatical accuracy and language range are still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),

    ('needs_work', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in cohesion and in grammatical accuracy and language range. '
        'However, the organisation and clear presentation of written work and the ability to adapt tone and style '
        'appropriately remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in cohesion and in grammatical accuracy and language range, '
        'while control of register is still developing. However, the organisation and clear presentation of '
        'written work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in cohesion, grammatical accuracy and language range, and '
        'control of register. However, the organisation and clear presentation of written work remain less '
        'established and are the main area requiring further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion and grammatical accuracy and language range meet the expected standard. However, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion and grammatical accuracy and language range meet the expected standard. However, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),

    ('needs_work', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while cohesion meets '
        'the expected standard. However, the organisation and clear presentation of written work and control of '
        'register remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while cohesion meets '
        'the expected standard. Control of register is still developing; however, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while cohesion and '
        'control of register meet the expected standard. However, the organisation and clear presentation of '
        'written work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context. Cohesion meets the expected standard; however, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. Cohesion meets the '
        'expected standard; however, the organisation and clear presentation of written work remain less '
        'established and require further development.'
    ),

    ('needs_work', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while cohesion meets '
        'the expected standard. However, the organisation and clear presentation of written work and control of '
        'register remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while cohesion meets '
        'the expected standard. Control of register is still developing; however, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while cohesion and '
        'control of register meet the expected standard. However, the organisation and clear presentation of '
        'written work remain less established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Cohesion meets the '
        'expected standard; however, the organisation and clear presentation of written work remain less '
        'established and require further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. Cohesion meets the expected standard; however, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence. '
        'However, the organisation and clear presentation of written work, grammatical accuracy and language '
        'range, and control of register remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'control of register is still developing. However, the organisation of written work and grammatical '
        'accuracy and language range remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'the ability to adapt tone and style appropriately meets the expected standard. However, the organisation '
        'of written work and control of grammar and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in both cohesion and the ability to adapt tone and style '
        'appropriately to purpose, audience and context. However, the organisation and clear presentation of '
        'written work and grammatical accuracy and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in connecting ideas logically and maintaining coherence. '
        'However, the organisation of written work and control of grammar and language range remain less '
        'established and require further development.'
    ),

    ('needs_work', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range are still developing. However, the organisation of written work '
        'and control of register remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion. Grammatical accuracy and language range and control '
        'of register are still developing, while the organisation and clear presentation of written work remain '
        'less established and require further development.'
    ),
    ('needs_work', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'control of register meets the expected standard. Grammatical accuracy and language range are still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context. Grammatical accuracy and language range are still developing; however, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Grammatical accuracy and language range are still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),

    ('needs_work', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range meet the expected standard. However, the organisation and clear '
        'presentation of written work and control of register remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion, while grammatical accuracy and language range meet '
        'the expected standard. Control of register is still developing; however, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range and control of register meet the expected standard. However, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context, while grammatical accuracy and language range meet the expected standard. '
        'However, the organisation and clear presentation of written work remain less established and require '
        'further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Grammatical accuracy and language range meet the '
        'expected standard; however, the organisation and clear presentation of written work remain less '
        'established and require further development.'
    ),

    ('needs_work', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence and in '
        'using grammar and vocabulary with accuracy and range. However, the organisation and clear presentation '
        'of written work and control of register remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'control of register is still developing. However, the organisation and clear presentation of written '
        'work remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'the ability to adapt tone and style appropriately meets the expected standard. However, the organisation '
        'and clear presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, the organisation '
        'and clear presentation of written work remain less established and are the main area requiring further '
        'development.'
    ),
    ('needs_work', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in cohesion and in grammatical accuracy and language range. '
        'However, the organisation and clear presentation of written work remain less established and require '
        'further development.'
    ),

    ('needs_work', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in connecting ideas logically and maintaining coherence. However, the organisation and clear '
        'presentation of written work and control of register remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion. Control of register is still developing; however, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion, while control of register meets the expected standard. However, the organisation '
        'and clear presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and demonstrates '
        'confidence in both cohesion and the ability to adapt tone and style appropriately. However, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in connecting '
        'ideas logically and maintaining coherence. However, the organisation and clear presentation of written '
        'work remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence. '
        'However, the organisation and clear presentation of written work, grammatical accuracy and language '
        'range, and control of register remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in cohesion, while control of register is still developing. '
        'However, the organisation of written work and grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'the ability to adapt tone and style appropriately meets the expected standard. However, the organisation '
        'of written work and control of grammar and language range remain less established and require further '
        'development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. However, the organisation of written work and '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context. However, the organisation and clear presentation of written work and control of '
        'grammar and language range remain less established and require further development.'
    ),

    ('needs_work', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range are still developing. However, the organisation of written work '
        'and control of register remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in cohesion. Grammatical accuracy and language range and control '
        'of register are still developing, while the organisation and clear presentation of written work remain '
        'less established and require further development.'
    ),
    ('needs_work', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion, while control of register meets the expected standard. '
        'Grammatical accuracy and language range are still developing; however, the organisation and clear '
        'presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Grammatical accuracy and language range are still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context. Grammatical accuracy and language range are still developing; however, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),

    ('needs_work', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion, while grammatical accuracy and language range meet '
        'the expected standard. However, the organisation and clear presentation of written work and control of '
        'register remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range meet the expected standard. Control of register is still '
        'developing; however, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion, while grammatical accuracy and language range and '
        'control of register meet the expected standard. However, the organisation and clear presentation of '
        'written work remain less established and are the main area requiring further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Grammatical accuracy and language range meet the '
        'expected standard; however, the organisation and clear presentation of written work remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while grammatical accuracy and language range meet the expected standard. However, '
        'the organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),

    ('needs_work', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range. However, the organisation and clear presentation of written work and '
        'control of register remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range. Control of register is still developing; however, the organisation and '
        'clear presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in grammatical accuracy '
        'and language range, while the ability to adapt tone and style appropriately meets the expected standard. '
        'However, the organisation and clear presentation of written work remain less established and require '
        'further development.'
    ),
    ('needs_work', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence and also '
        'demonstrates confidence in grammatical accuracy and language range and in adapting tone and style '
        'appropriately. However, the organisation and clear presentation of written work remain less established '
        'and require further development.'
    ),
    ('needs_work', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in grammatical accuracy and language range. '
        'However, the organisation and clear presentation of written work remain less established and require '
        'further development.'
    ),

    ('needs_work', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range. '
        'However, the organisation and clear presentation of written work and control of register remain less '
        'established and require further development.'
    ),
    ('needs_work', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in connecting ideas logically and maintaining coherence and in '
        'grammatical accuracy and language range. Control of register is still developing; however, the '
        'organisation and clear presentation of written work remain less established and require further '
        'development.'
    ),
    ('needs_work', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'the ability to adapt tone and style appropriately meets the expected standard. However, the organisation '
        'and clear presentation of written work remain less established and require further development.'
    ),
    ('needs_work', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range and also '
        'demonstrates confidence in adapting tone and style appropriately to purpose, audience and context. '
        'However, the organisation and clear presentation of written work remain less established and require '
        'further development.'
    ),
    ('needs_work', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, the organisation '
        'and clear presentation of written work remain less established and are the main area requiring further '
        'development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} is developing greater ability to organise written work and present ideas clearly. '
        'However, cohesion, grammatical accuracy and language range, and control of register remain less '
        'established and require further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} is developing greater control over the organisation of written work and the use of '
        'appropriate tone and style. However, the ability to connect ideas coherently and control grammar and '
        'language range remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context, '
        'while the organisation and clear presentation of written work are still developing. However, cohesion '
        'and grammatical accuracy and language range remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while the organisation of written work is still developing. However, cohesion and grammatical '
        'accuracy and language range remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. The organisation and clear presentation of written work are still developing; however, cohesion '
        'and grammatical accuracy and language range remain less established and require further development.'
    ),

    ('developing', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} is developing greater control over the organisation of written work and over grammatical '
        'accuracy and language range. However, cohesion and the ability to adapt tone and style appropriately '
        'remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'developing', 'developing'): (
        '{learner_name} is developing greater control of organisation, grammatical accuracy and language range, '
        'and register. However, the ability to connect ideas logically and maintain coherence remains less '
        'established and requires further development.'
    ),
    ('developing', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context. '
        'The organisation of written work and grammatical accuracy and language range are still developing; '
        'however, cohesion remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context. Organisation and grammatical accuracy and language range are still developing; however, the '
        'ability to connect ideas coherently remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. Organisation and grammatical accuracy and language range are still developing; however, '
        'cohesion remains less established and requires further development.'
    ),

    ('developing', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while the '
        'organisation and clear presentation of written work are still developing. However, cohesion and control '
        'of register remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range. Organisation and '
        'control of register are still developing; however, the ability to connect ideas logically and maintain '
        'coherence remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range and in adapting '
        'tone and style appropriately to purpose, audience and context. The organisation of written work is still '
        'developing; however, cohesion remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. Organisation is still '
        'developing; however, cohesion remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. The organisation and '
        'clear presentation of written work are still developing; however, cohesion remains less established and '
        'requires further development.'
    ),

    ('developing', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while the organisation '
        'and clear presentation of written work are still developing. However, cohesion and control of register '
        'remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range. Organisation and '
        'control of register are still developing; however, cohesion remains less established and requires '
        'further development.'
    ),
    ('developing', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while control of '
        'register meets the expected standard. The organisation and clear presentation of written work are still '
        'developing; however, cohesion remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context. Organisation is still developing; however, '
        'the ability to connect ideas logically and maintain coherence remains less established and requires '
        'further development.'
    ),
    ('developing', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. The organisation '
        'and clear presentation of written work are still developing; however, cohesion remains less established '
        'and requires further development.'
    ),

    ('developing', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while the organisation '
        'and clear presentation of written work are still developing. However, cohesion and control of register '
        'remain less established and require further development.'
    ),
    ('developing', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range. Organisation and '
        'control of register are still developing; however, cohesion remains less established and requires '
        'further development.'
    ),
    ('developing', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while control of '
        'register meets the expected standard. The organisation and clear presentation of written work are still '
        'developing; however, cohesion remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Organisation is '
        'still developing; however, cohesion remains less established and requires further development.'
    ),
    ('developing', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. The organisation and clear presentation of written '
        'work are still developing; however, cohesion remains less established and is the main area requiring '
        'further development.'
    ),
    ('developing', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} is developing greater control over the organisation of written work and the ability to '
        'connect ideas coherently. However, grammatical accuracy and language range and control of register '
        'remain less established and require further development.'
    ),
    ('developing', 'developing', 'needs_work', 'developing'): (
        '{learner_name} is developing greater control of organisation, cohesion and register. However, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('developing', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context. '
        'Organisation and cohesion are still developing; however, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('developing', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context. Organisation and cohesion are still developing; however, grammatical accuracy and language '
        'range remain less established and require further development.'
    ),
    ('developing', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. Organisation and cohesion are still developing; however, grammatical accuracy and language '
        'range remain less established and require further development.'
    ),

    ('developing', 'developing', 'developing', 'needs_work'): (
        '{learner_name} is developing greater control of organisation, cohesion, and grammatical accuracy and '
        'language range. However, the ability to adapt tone and style appropriately remains less established and '
        'requires further development.'
    ),
    ('developing', 'developing', 'developing', 'developing'): (
        "{learner_name}'s writing skills are still developing across all four assessed areas. Further "
        'consolidation of organisation and clarity, cohesion, grammatical accuracy and language range, and '
        'control of register will help bring written performance more consistently to the expected standard.'
    ),
    ('developing', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in adapting tone and style to purpose, audience and context, '
        'while organisation, cohesion, and grammatical accuracy and language range are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation, cohesion, and grammatical accuracy and language range are still developing '
        'and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context. By contrast, organisation, cohesion, and grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),

    ('developing', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range, while organisation '
        'and cohesion are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range. Organisation, '
        'cohesion and control of register are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in grammatical accuracy and language range and in adapting '
        'tone and style appropriately to purpose, audience and context. However, organisation and cohesion are '
        'still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. Organisation and '
        'cohesion are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while grammatical accuracy and language range meet the expected standard. Organisation and '
        'cohesion are still developing and would benefit from further consolidation.'
    ),

    ('developing', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'and cohesion are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range. Organisation, '
        'cohesion and control of register are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while control of '
        'register meets the expected standard. Organisation and cohesion are still developing and would benefit '
        'from further consolidation.'
    ),
    ('developing', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context. However, organisation and cohesion are still '
        'developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. Organisation and '
        'cohesion are still developing and would benefit from further consolidation.'
    ),

    ('developing', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation and '
        'cohesion are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range. Organisation, cohesion '
        'and control of register are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while control of '
        'register meets the expected standard. Organisation and cohesion are still developing and would benefit '
        'from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Organisation and '
        'cohesion are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. However, organisation and cohesion are still '
        'developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in connecting ideas logically and maintaining coherence, '
        'while the organisation and clear presentation of written work are still developing. However, '
        'grammatical accuracy and language range and control of register remain less established and require '
        'further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in cohesion. Organisation and control of register are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context. The organisation and clear presentation of written work are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. Organisation is still developing; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. The organisation and clear presentation of written '
        'work are still developing; however, grammatical accuracy and language range remain less established and '
        'require further development.'
    ),

    ('developing', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in cohesion, while organisation and grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in connecting ideas logically and maintaining coherence. '
        'Organisation, grammatical accuracy and language range, and control of register are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context. Organisation and grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. Organisation and grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion meets the expected standard. Organisation and grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),

    ('developing', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in cohesion and in grammatical accuracy and language range, '
        'while the organisation and clear presentation of written work are still developing. However, control '
        'of register remains less established and requires further development.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in cohesion and in grammatical accuracy and language range. '
        'Organisation and control of register are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in cohesion, grammatical accuracy and language range, and '
        'control of register. However, the organisation and clear presentation of written work are still '
        'developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion and grammatical accuracy and language range meet the expected standard. '
        'Organisation is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while cohesion and grammatical accuracy and language range meet the expected standard. '
        'Organisation is still developing and would benefit from further consolidation.'
    ),

    ('developing', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while cohesion meets '
        'the expected standard and organisation is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('developing', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while cohesion meets '
        'the expected standard. Organisation and control of register are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while cohesion and '
        'control of register meet the expected standard. The organisation and clear presentation of written work '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context. Cohesion meets the expected standard, while '
        'organisation is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. Cohesion meets the '
        'expected standard, while the organisation and clear presentation of written work are still developing '
        'and would benefit from further consolidation.'
    ),

    ('developing', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while cohesion meets '
        'the expected standard and organisation is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('developing', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while cohesion meets '
        'the expected standard. Organisation and control of register are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while cohesion and '
        'control of register meet the expected standard. The organisation and clear presentation of written work '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Cohesion meets the '
        'expected standard, while organisation is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. Cohesion also meets the expected standard, while '
        'the organisation and clear presentation of written work are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'the organisation and clear presentation of written work are still developing. However, grammatical '
        'accuracy and language range and control of register remain less established and require further '
        'development.'
    ),
    ('developing', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion. Organisation and control of register are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('developing', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'control of register meets the expected standard. The organisation and clear presentation of written '
        'work are still developing; however, grammatical accuracy and language range remain less established '
        'and require further development.'
    ),
    ('developing', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context. Organisation is still developing; however, grammatical accuracy and '
        'language range remain less established and require further development.'
    ),
    ('developing', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. The organisation and clear presentation of '
        'written work are still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),

    ('developing', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation and grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence. '
        'Organisation, grammatical accuracy and language range, and control of register are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion, while control of register meets the expected '
        'standard. Organisation and grammatical accuracy and language range are still developing and would '
        'benefit from further consolidation.'
    ),
    ('developing', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context. However, organisation and grammatical accuracy and language range are '
        'still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Organisation and grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),

    ('developing', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in cohesion, while grammatical accuracy and language range meet '
        'the expected standard and organisation is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('developing', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range meet the expected standard. Organisation and control of register '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion, while grammatical accuracy and language range and '
        'control of register meet the expected standard. The organisation and clear presentation of written work '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context, while grammatical accuracy and language range meet the expected standard. '
        'Organisation is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Grammatical accuracy and language range meet the '
        'expected standard, while the organisation and clear presentation of written work are still developing '
        'and would benefit from further consolidation.'
    ),

    ('developing', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'organisation is still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range. '
        'Organisation and control of register are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'control of register meets the expected standard. The organisation and clear presentation of written work '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, the organisation '
        'and clear presentation of written work are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in cohesion and in grammatical accuracy and language range. '
        'The organisation and clear presentation of written work are still developing and would benefit from '
        'further consolidation.'
    ),

    ('developing', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion. Organisation is still developing; however, control of register remains less '
        'established and requires further development.'
    ),
    ('developing', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion. Organisation and control of register are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion, while control of register meets the expected standard. The organisation and '
        'clear presentation of written work are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and demonstrates '
        'confidence in both cohesion and the ability to adapt tone and style appropriately. However, the '
        'organisation and clear presentation of written work are still developing and would benefit from further '
        'consolidation.'
    ),
    ('developing', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in cohesion. '
        'The organisation and clear presentation of written work are still developing and would benefit from '
        'further consolidation.'
    ),

    ('developing', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while the '
        'organisation and clear presentation of written work are still developing. However, grammatical accuracy '
        'and language range and control of register remain less established and require further development.'
    ),
    ('developing', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in cohesion. Organisation and control of register are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('developing', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'control of register meets the expected standard. The organisation and clear presentation of written '
        'work are still developing; however, grammatical accuracy and language range remain less established '
        'and require further development.'
    ),
    ('developing', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Organisation is still developing; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('developing', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context. The organisation and clear presentation of written work are still developing; '
        'however, grammatical accuracy and language range remain less established and require further development.'
    ),

    ('developing', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion, while organisation and grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence. '
        'Organisation, grammatical accuracy and language range, and control of register are still developing and '
        'would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion, while control of register meets the expected standard. '
        'Organisation and grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('developing', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Organisation and grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context. However, organisation and grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),

    ('developing', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion, while grammatical accuracy and language range meet '
        'the expected standard and organisation is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('developing', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'grammatical accuracy and language range meet the expected standard. Organisation and control of register '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion, while grammatical accuracy and language range and '
        'control of register meet the expected standard. The organisation and clear presentation of written work '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Grammatical accuracy and language range meet the '
        'expected standard, while organisation is still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while grammatical accuracy and language range meet the expected standard. The '
        'organisation and clear presentation of written work are still developing and would benefit from further '
        'consolidation.'
    ),

    ('developing', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range. Organisation is still developing; however, control of register remains '
        'less established and requires further development.'
    ),
    ('developing', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range. Organisation and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in grammatical accuracy '
        'and language range, while control of register meets the expected standard. The organisation and clear '
        'presentation of written work are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range and in adapting tone and style appropriately. However, the organisation and '
        'clear presentation of written work are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in grammatical accuracy and language range. '
        'The organisation and clear presentation of written work are still developing and would benefit from '
        'further consolidation.'
    ),

    ('developing', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'organisation is still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('developing', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range. '
        'Organisation and control of register are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'control of register meets the expected standard. The organisation and clear presentation of written work '
        'are still developing and would benefit from further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range and also '
        'demonstrates confidence in adapting tone and style appropriately to purpose, audience and context. '
        'However, the organisation and clear presentation of written work are still developing and would benefit '
        'from further consolidation.'
    ),
    ('developing', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, the organisation '
        'and clear presentation of written work are still developing and remain the principal area for further '
        'consolidation.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in the organisation and clear presentation of written work. '
        'However, cohesion, grammatical accuracy and language range, and control of register remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in organising written work and presenting ideas clearly, '
        'while control of register is still developing. However, cohesion and grammatical accuracy and language '
        'range remain less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation and in adapting tone and style appropriately '
        'to purpose, audience and context. However, cohesion and grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. However, cohesion and grammatical accuracy and '
        'language range remain less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while the organisation and clear presentation of written work meet the expected standard. '
        'However, cohesion and grammatical accuracy and language range remain less established and require '
        'further development.'
    ),

    ('satisfactory', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in organisation, while grammatical accuracy and language '
        'range are still developing. However, cohesion and control of register remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in organising written work and presenting ideas clearly. '
        'Grammatical accuracy and language range and control of register are still developing; however, cohesion '
        'remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation and in adapting tone and style appropriately '
        'to purpose, audience and context. Grammatical accuracy and language range are still developing; however, '
        'cohesion remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. Grammatical accuracy and language range are '
        'still developing; however, cohesion remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. Grammatical accuracy and language range are '
        'still developing; however, cohesion remains less established and requires further development.'
    ),

    ('satisfactory', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in organisation and in grammatical accuracy and language '
        'range. However, cohesion and control of register remain less established and require further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in organisation and in grammatical accuracy and language '
        'range, while control of register is still developing. However, cohesion remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation, grammatical accuracy and language range, '
        'and control of register. However, cohesion remains less established and is the main area requiring '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and grammatical accuracy and language range meet the expected standard. '
        'However, cohesion remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and grammatical accuracy and language range meet the expected standard. '
        'However, cohesion remains less established and requires further development.'
    ),

    ('satisfactory', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'meets the expected standard. However, cohesion and control of register remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'meets the expected standard. Control of register is still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'and control of register meet the expected standard. However, cohesion remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context, while organisation meets the expected '
        'standard. However, cohesion remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. Organisation meets '
        'the expected standard; however, cohesion remains less established and requires further development.'
    ),

    ('satisfactory', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation '
        'meets the expected standard. However, cohesion and control of register remain less established and '
        'require further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation '
        'meets the expected standard. Control of register is still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation '
        'and control of register meet the expected standard. However, cohesion remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Organisation meets '
        'the expected standard; however, cohesion remains less established and requires further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while organisation meets the expected standard. '
        'However, cohesion remains less established and is the main area requiring further development.'
    ),

    ('satisfactory', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} meets the expected standard in the organisation and clear presentation of written work, '
        'while cohesion is still developing. However, grammatical accuracy and language range and control of '
        'register remain less established and require further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in organisation. Cohesion and control of register are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation and in adapting tone and style appropriately '
        'to purpose, audience and context. Cohesion is still developing; however, grammatical accuracy and '
        'language range remain less established and require further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. Cohesion is still developing; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. Cohesion is still developing; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),

    ('satisfactory', 'developing', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in organisation, while cohesion and grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in organising written work and presenting ideas clearly. '
        'Cohesion, grammatical accuracy and language range, and control of register are still developing and '
        'would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation and in adapting tone and style appropriately '
        'to purpose, audience and context, while cohesion and grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. Cohesion and grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation meets the expected standard. Cohesion and grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),

    ('satisfactory', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} meets the expected standard in organisation and in grammatical accuracy and language '
        'range, while cohesion is still developing. However, control of register remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in organisation and in grammatical accuracy and language '
        'range. Cohesion and control of register are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation, grammatical accuracy and language range, '
        'and control of register. However, cohesion is still developing and would benefit from further '
        'consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and grammatical accuracy and language range meet the expected standard. '
        'Cohesion is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and grammatical accuracy and language range meet the expected standard. '
        'Cohesion is still developing and would benefit from further consolidation.'
    ),

    ('satisfactory', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'meets the expected standard and cohesion is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'meets the expected standard. Cohesion and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'and control of register meet the expected standard. Cohesion is still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context, while organisation meets the expected standard. '
        'Cohesion is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. Organisation meets '
        'the expected standard, while cohesion is still developing and would benefit from further consolidation.'
    ),

    ('satisfactory', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation '
        'meets the expected standard and cohesion is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation '
        'meets the expected standard. Cohesion and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation '
        'and control of register meet the expected standard. Cohesion is still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Organisation meets '
        'the expected standard, while cohesion is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. Organisation also meets the expected standard, '
        'while cohesion is still developing and remains the main area for further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s writing meets the expected standard in organisation and cohesion. However, grammatical "
        'accuracy and language range and control of register remain less established and require further '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} meets the expected standard in organisation and cohesion, while control of register is '
        'still developing. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation, cohesion and control of register. However, '
        'grammatical accuracy and language range remain less established and are the main area requiring further '
        'development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and cohesion meet the expected standard. However, grammatical accuracy and '
        'language range remain less established and require further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and cohesion meet the expected standard. However, grammatical accuracy and '
        'language range remain less established and require further development.'
    ),

    ('satisfactory', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} meets the expected standard in organisation and cohesion, while grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} meets the expected standard in organisation and cohesion. Grammatical accuracy and '
        'language range and control of register are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} meets the expected standard in organisation, cohesion and control of register, while '
        'grammatical accuracy and language range are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and cohesion meet the expected standard. Grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation and cohesion meet the expected standard. Grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),

    ('satisfactory', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s writing meets the expected standard in organisation, cohesion, and grammatical accuracy "
        'and language range. However, control of register remains less established and is the main area requiring '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} meets the expected standard in organisation, cohesion, and grammatical accuracy and '
        'language range. Control of register is still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s writing performance meets the expected standard across all four assessed areas. "
        'Organisation and clarity, cohesion, grammatical accuracy and language range, and control of register '
        'are satisfactory for this level, although there remains clear scope to develop greater consistency, '
        'flexibility and precision.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation, cohesion, and grammatical accuracy and language range meet the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while organisation, cohesion, and grammatical accuracy and language range meet the expected '
        'standard, with further scope for development.'
    ),

    ('satisfactory', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'and cohesion meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation '
        'and cohesion meet the expected standard. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range, while organisation, '
        'cohesion and control of register meet the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context, while organisation and cohesion meet the '
        'expected standard.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in grammatical accuracy and language range. Organisation and '
        'cohesion meet the expected standard, with further scope for development.'
    ),

    ('satisfactory', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation and '
        'cohesion meet the expected standard. However, control of register remains less established and requires '
        'further development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation and '
        'cohesion meet the expected standard. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while organisation, '
        'cohesion and control of register meet the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in adapting tone and style appropriately to purpose, audience and context. Organisation and '
        'cohesion meet the expected standard.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while organisation and cohesion meet the expected '
        'standard, with further scope for development.'
    ),

    ('satisfactory', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'organisation meets the expected standard. However, grammatical accuracy and language range and control '
        'of register remain less established and require further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation meets the expected standard and '
        'control of register is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation and control of register meet the '
        'expected standard. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context, while organisation meets the expected standard. However, grammatical '
        'accuracy and language range remain less established and require further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Organisation meets the expected standard; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),

    ('satisfactory', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation meets the expected standard and '
        'grammatical accuracy and language range are still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'organisation meets the expected standard. Grammatical accuracy and language range and control of '
        'register are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation and control of register meet the '
        'expected standard. Grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context, while organisation meets the expected standard. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Organisation meets the expected standard, while '
        'grammatical accuracy and language range are still developing and would benefit from further consolidation.'
    ),

    ('satisfactory', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation and grammatical accuracy and '
        'language range meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion, while organisation and grammatical accuracy and '
        'language range meet the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in connecting ideas logically and maintaining coherence, while '
        'organisation, grammatical accuracy and language range, and control of register meet the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion and in adapting tone and style appropriately to '
        'purpose, audience and context, while organisation and grammatical accuracy and language range meet the '
        'expected standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in cohesion. Organisation and grammatical accuracy and language '
        'range meet the expected standard, with further scope for development.'
    ),

    ('satisfactory', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'organisation meets the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'organisation meets the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in cohesion and in grammatical accuracy and language range, while '
        'organisation and control of register meet the expected standard.'
    ),
    ('satisfactory', 'confident', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. Organisation meets the '
        'expected standard, with further scope for development.'
    ),
    ('satisfactory', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in cohesion and in grammatical accuracy and language range. '
        'Organisation meets the expected standard, with further scope for development.'
    ),

    ('satisfactory', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion. Organisation meets the expected standard; however, control of register remains '
        'less established and requires further development.'
    ),
    ('satisfactory', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion. Organisation meets the expected standard, while control of register is still '
        'developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in cohesion, while organisation and control of register meet the expected standard.'
    ),
    ('satisfactory', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and demonstrates '
        'confidence in both cohesion and the ability to adapt tone and style appropriately. Organisation meets '
        'the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in cohesion. '
        'Organisation meets the expected standard, with further scope for development.'
    ),

    ('satisfactory', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'organisation meets the expected standard. However, grammatical accuracy and language range and control '
        'of register remain less established and require further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in cohesion, while organisation meets the expected standard and '
        'control of register is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion, while organisation and control of register meet the '
        'expected standard. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Organisation meets the expected standard; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context. Organisation meets the expected standard; however, grammatical accuracy and '
        'language range remain less established and require further development.'
    ),

    ('satisfactory', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion, while organisation meets the expected standard and '
        'grammatical accuracy and language range are still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('satisfactory', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'organisation meets the expected standard. Grammatical accuracy and language range and control of '
        'register are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion, while organisation and control of register meet the '
        'expected standard. Grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('satisfactory', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Organisation meets the expected standard, while '
        'grammatical accuracy and language range are still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while organisation meets the expected standard. Grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),

    ('satisfactory', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion, while organisation and grammatical accuracy and '
        'language range meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in cohesion, while organisation and grammatical accuracy and '
        'language range meet the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'organisation, grammatical accuracy and language range, and control of register meet the expected '
        'standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in adapting tone and '
        'style appropriately to purpose, audience and context. Organisation and grammatical accuracy and language '
        'range meet the expected standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while organisation and grammatical accuracy and language range meet the expected '
        'standard, with further scope for development.'
    ),

    ('satisfactory', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range. Organisation meets the expected standard; however, control of register '
        'remains less established and requires further development.'
    ),
    ('satisfactory', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range. Organisation meets the expected standard, while control of register is '
        'still developing and would benefit from further consolidation.'
    ),
    ('satisfactory', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in grammatical accuracy '
        'and language range, while organisation and control of register meet the expected standard.'
    ),
    ('satisfactory', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in grammatical '
        'accuracy and language range and in adapting tone and style appropriately. Organisation meets the '
        'expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in grammatical accuracy and language range. '
        'Organisation meets the expected standard, with further scope for development.'
    ),

    ('satisfactory', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'organisation meets the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('satisfactory', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'organisation meets the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('satisfactory', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'organisation and control of register meet the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range and also '
        'demonstrates confidence in adapting tone and style appropriately to purpose, audience and context. '
        'Organisation meets the expected standard, with further scope for development.'
    ),
    ('satisfactory', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. Organisation also meets '
        'the expected standard, with further scope to develop greater consistency and sophistication.'
    ),
    ('confident', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly. '
        'However, cohesion, grammatical accuracy and language range, and control of register remain less '
        'established and require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in the organisation and clear presentation of written work, while '
        'control of register is still developing. However, cohesion and grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while control of register meets the expected '
        'standard. However, cohesion and grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in both the organisation of written work and the ability to adapt '
        'tone and style appropriately to purpose, audience and context. However, cohesion and grammatical '
        'accuracy and language range remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organising written work and presenting ideas clearly. '
        'However, cohesion and grammatical accuracy and language range remain less established and require '
        'further development.'
    ),

    ('confident', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, while grammatical accuracy and language range '
        'are still developing. However, cohesion and control of register remain less established and require '
        'further development.'
    ),
    ('confident', 'needs_work', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly. '
        'Grammatical accuracy and language range and control of register are still developing; however, cohesion '
        'remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while control of register meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('confident', 'needs_work', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. Grammatical accuracy and language range are still developing; however, '
        'cohesion remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Grammatical accuracy and language range are '
        'still developing; however, cohesion remains less established and requires further development.'
    ),

    ('confident', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, while grammatical accuracy and language range '
        'meet the expected standard. However, cohesion and control of register remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in organisation, while grammatical accuracy and language range '
        'meet the expected standard. Control of register is still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly, while '
        'grammatical accuracy and language range and control of register meet the expected standard. However, '
        'cohesion remains less established and is the main area requiring further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while grammatical accuracy and language range meet the expected standard. '
        'However, cohesion remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Grammatical accuracy and language range meet '
        'the expected standard; however, cohesion remains less established and requires further development.'
    ),

    ('confident', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range. '
        'However, cohesion and control of register remain less established and require further development.'
    ),
    ('confident', 'needs_work', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range. '
        'Control of register is still developing; however, cohesion remains less established and requires further '
        'development.'
    ),
    ('confident', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range, '
        'while control of register meets the expected standard. However, cohesion remains less established and '
        'requires further development.'
    ),
    ('confident', 'needs_work', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, cohesion remains '
        'less established and is the main area requiring further development.'
    ),
    ('confident', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in organisation and in grammatical accuracy and language '
        'range. However, cohesion remains less established and requires further development.'
    ),

    ('confident', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation. However, cohesion and control of register remain less established and '
        'require further development.'
    ),
    ('confident', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation. Control of register is still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('confident', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation, while control of register meets the expected standard. However, cohesion '
        'remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and demonstrates '
        'confidence in both organisation and the ability to adapt tone and style appropriately. However, cohesion '
        'remains less established and requires further development.'
    ),
    ('confident', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in organisation. '
        'However, cohesion remains less established and is the main area requiring further development.'
    ),

    ('confident', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly, while '
        'cohesion is still developing. However, grammatical accuracy and language range and control of register '
        'remain less established and require further development.'
    ),
    ('confident', 'developing', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in organisation. Cohesion and control of register are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('confident', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while control of register meets the expected '
        'standard. Cohesion is still developing; however, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('confident', 'developing', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. Cohesion is still developing; however, grammatical accuracy and language '
        'range remain less established and require further development.'
    ),
    ('confident', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Cohesion is still developing; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),

    ('confident', 'developing', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion and grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('confident', 'developing', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly. '
        'Cohesion, grammatical accuracy and language range, and control of register are still developing and '
        'would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while control of register meets the expected '
        'standard. Cohesion and grammatical accuracy and language range are still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'developing', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. Cohesion and grammatical accuracy and language range are still developing '
        'and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Cohesion and grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),

    ('confident', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, while grammatical accuracy and language range '
        'meet the expected standard and cohesion is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('confident', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in organisation, while grammatical accuracy and language range '
        'meet the expected standard. Cohesion and control of register are still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while grammatical accuracy and language range '
        'and control of register meet the expected standard. Cohesion is still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while grammatical accuracy and language range meet the expected standard. '
        'Cohesion is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Grammatical accuracy and language range meet '
        'the expected standard, while cohesion is still developing and would benefit from further consolidation.'
    ),

    ('confident', 'developing', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range, '
        'while cohesion is still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('confident', 'developing', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range. '
        'Cohesion and control of register are still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range, '
        'while control of register meets the expected standard. Cohesion is still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'developing', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, cohesion is '
        'still developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in organisation and in grammatical accuracy and language '
        'range. Cohesion is still developing and would benefit from further consolidation.'
    ),

    ('confident', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation, while cohesion is still developing. However, control of register remains '
        'less established and requires further development.'
    ),
    ('confident', 'developing', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation. Cohesion and control of register are still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation, while control of register meets the expected standard. Cohesion is still '
        'developing and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and demonstrates '
        'confidence in organisation and in adapting tone and style appropriately. Cohesion is still developing '
        'and would benefit from further consolidation.'
    ),
    ('confident', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in organisation. '
        'Cohesion is still developing and remains the principal area for further consolidation.'
    ),

    ('confident', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly, while '
        'cohesion meets the expected standard. However, grammatical accuracy and language range and control of '
        'register remain less established and require further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion meets the expected standard and '
        'control of register is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion and control of register meet the '
        'expected standard. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while cohesion meets the expected standard. However, grammatical accuracy '
        'and language range remain less established and require further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Cohesion meets the expected standard; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),

    ('confident', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion meets the expected standard and '
        'grammatical accuracy and language range are still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('confident', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion meets the expected standard. '
        'Grammatical accuracy and language range and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion and control of register meet the '
        'expected standard. Grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while cohesion meets the expected standard. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Cohesion meets the expected standard, while '
        'grammatical accuracy and language range are still developing and would benefit from further consolidation.'
    ),

    ('confident', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion and grammatical accuracy and '
        'language range meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in organisation, while cohesion and grammatical accuracy and '
        'language range meet the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organising written work and presenting ideas clearly, while '
        'cohesion, grammatical accuracy and language range, and control of register meet the expected standard, '
        'with further scope for development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while cohesion and grammatical accuracy and language range meet the '
        'expected standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context and also demonstrates confidence in organisation. Cohesion and grammatical accuracy and language '
        'range meet the expected standard, with further scope for development.'
    ),

    ('confident', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range, '
        'while cohesion meets the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('confident', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range, '
        'while cohesion meets the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation and in grammatical accuracy and language range, '
        'while cohesion and control of register meet the expected standard.'
    ),
    ('confident', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} demonstrates confidence in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. Cohesion meets the '
        'expected standard, with further scope for development.'
    ),
    ('confident', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in organisation and in grammatical accuracy and language '
        'range. Cohesion meets the expected standard, with further scope for development.'
    ),

    ('confident', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation, while cohesion meets the expected standard. However, control of register '
        'remains less established and requires further development.'
    ),
    ('confident', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation, while cohesion meets the expected standard. Control of register is still '
        'developing and would benefit from further consolidation.'
    ),
    ('confident', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation, while cohesion and control of register meet the expected standard.'
    ),
    ('confident', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and demonstrates '
        'confidence in organisation and in adapting tone and style appropriately. Cohesion meets the expected '
        'standard, with further scope for development.'
    ),
    ('confident', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in organisation. '
        'Cohesion meets the expected standard, with further scope for development.'
    ),
    ('confident', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates confidence in both the organisation of written work and the ability to '
        'connect ideas logically and maintain coherence. However, grammatical accuracy and language range and '
        'control of register remain less established and require further development.'
    ),
    ('confident', 'confident', 'needs_work', 'developing'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while control of register is still '
        'developing. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('confident', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while control of register meets the '
        'expected standard. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('confident', 'confident', 'needs_work', 'confident'): (
        '{learner_name} demonstrates confidence in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context. However, grammatical accuracy and language range remain '
        'less established and are the main area requiring further development.'
    ),
    ('confident', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in organisation and cohesion. However, grammatical accuracy '
        'and language range remain less established and require further development.'
    ),

    ('confident', 'confident', 'developing', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('confident', 'confident', 'developing', 'developing'): (
        '{learner_name} demonstrates confidence in organisation and cohesion. Grammatical accuracy and language '
        'range and control of register are still developing and would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while control of register meets the '
        'expected standard. Grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'confident', 'developing', 'confident'): (
        '{learner_name} demonstrates confidence in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context. However, grammatical accuracy and language range are '
        'still developing and would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'developing', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in organisation and cohesion. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),

    ('confident', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while grammatical accuracy and '
        'language range meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('confident', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while grammatical accuracy and '
        'language range meet the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('confident', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation and cohesion, while grammatical accuracy and '
        'language range and control of register meet the expected standard, with further scope for development.'
    ),
    ('confident', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates confidence in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context, while grammatical accuracy and language range meet the '
        'expected standard.'
    ),
    ('confident', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while also demonstrating confidence in organisation and cohesion. Grammatical accuracy and '
        'language range meet the expected standard, with further scope for development.'
    ),

    ('confident', 'confident', 'confident', 'needs_work'): (
        '{learner_name} demonstrates confidence in organisation, cohesion, and grammatical accuracy and language '
        'range. However, control of register remains less established and is the main area requiring further '
        'development.'
    ),
    ('confident', 'confident', 'confident', 'developing'): (
        '{learner_name} demonstrates confidence in organisation, cohesion, and grammatical accuracy and language '
        'range. Control of register is still developing and would benefit from further consolidation.'
    ),
    ('confident', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates confidence in organisation, cohesion, and grammatical accuracy and language '
        'range, while control of register meets the expected standard, with further scope for development.'
    ),
    ('confident', 'confident', 'confident', 'confident'): (
        '{learner_name} writes with confidence across all four assessed areas. Secure control is evident in the '
        'organisation and presentation of ideas, cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context.'
    ),
    ('confident', 'confident', 'confident', 'strong'): (
        '{learner_name} shows a clear strength in adapting tone and style appropriately to purpose, audience and '
        'context, while demonstrating confidence in organisation, cohesion, and grammatical accuracy and language '
        'range.'
    ),

    ('confident', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation and cohesion. However, control of register remains less established and '
        'requires further development.'
    ),
    ('confident', 'confident', 'strong', 'developing'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation and cohesion. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range and also demonstrates '
        'confidence in organisation and cohesion, while control of register meets the expected standard.'
    ),
    ('confident', 'confident', 'strong', 'confident'): (
        '{learner_name} shows a clear strength in grammatical accuracy and language range, while also '
        'demonstrating confidence in organisation, cohesion, and the ability to adapt tone and style appropriately '
        'to purpose, audience and context.'
    ),
    ('confident', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context, while also demonstrating confidence in organisation '
        'and cohesion.'
    ),

    ('confident', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence and also '
        'demonstrates confidence in organising written work and presenting ideas clearly. However, grammatical '
        'accuracy and language range and control of register remain less established and require further '
        'development.'
    ),
    ('confident', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'control of register is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('confident', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'control of register meets the expected standard. However, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('confident', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in both organisation and '
        'the ability to adapt tone and style appropriately. However, grammatical accuracy and language range '
        'remain less established and require further development.'
    ),
    ('confident', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in organisation. However, grammatical accuracy '
        'and language range remain less established and require further development.'
    ),

    ('confident', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'grammatical accuracy and language range are still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('confident', 'strong', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence and also '
        'demonstrates confidence in organisation. Grammatical accuracy and language range and control of register '
        'are still developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'control of register meets the expected standard. Grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in organisation and in '
        'adapting tone and style appropriately to purpose, audience and context. Grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in organisation. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),

    ('confident', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'grammatical accuracy and language range meet the expected standard. However, control of register remains '
        'less established and requires further development.'
    ),
    ('confident', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'grammatical accuracy and language range meet the expected standard. Control of register is still '
        'developing and would benefit from further consolidation.'
    ),
    ('confident', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and also demonstrates confidence in organisation, while '
        'grammatical accuracy and language range and control of register meet the expected standard, with further '
        'scope for development.'
    ),
    ('confident', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in organisation and in '
        'adapting tone and style appropriately to purpose, audience and context, while grammatical accuracy and '
        'language range meet the expected standard.'
    ),
    ('confident', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in organisation. Grammatical accuracy and '
        'language range meet the expected standard, with further scope for development.'
    ),

    ('confident', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in organisation and in '
        'grammatical accuracy and language range. However, control of register remains less established and '
        'requires further development.'
    ),
    ('confident', 'strong', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in organisation and in '
        'grammatical accuracy and language range. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in cohesion and demonstrates confidence in organisation and in '
        'grammatical accuracy and language range, while control of register meets the expected standard.'
    ),
    ('confident', 'strong', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in connecting ideas logically and maintaining coherence, while '
        'demonstrating confidence in organisation, grammatical accuracy and language range, and the ability to '
        'adapt tone and style appropriately to purpose, audience and context.'
    ),
    ('confident', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context, while also demonstrating confidence in organisation and in grammatical accuracy '
        'and language range.'
    ),

    ('confident', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range and also '
        'demonstrates confidence in organisation. However, control of register remains less established and '
        'requires further development.'
    ),
    ('confident', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range and also '
        'demonstrates confidence in organisation. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('confident', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'also demonstrating confidence in organisation. Control of register meets the expected standard, with '
        'further scope for development.'
    ),
    ('confident', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in cohesion and in grammatical accuracy and language range, while '
        'also demonstrating confidence in organisation and in adapting tone and style appropriately to purpose, '
        'audience and context.'
    ),
    ('confident', 'strong', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in cohesion, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context, while also demonstrating '
        'confidence in the organisation and clear presentation of written work.'
    ),

    ('strong', 'needs_work', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly. However, '
        'cohesion, grammatical accuracy and language range, and control of register remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in organisation, while control of register is still developing. '
        'However, cohesion and grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while control of register meets the expected '
        'standard. However, cohesion and grammatical accuracy and language range remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context. However, cohesion and grammatical accuracy and '
        'language range remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. However, cohesion and grammatical accuracy and language range remain less '
        'established and require further development.'
    ),

    ('strong', 'needs_work', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation, while grammatical accuracy and language range are '
        'still developing. However, cohesion and control of register remain less established and require further '
        'development.'
    ),
    ('strong', 'needs_work', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly. '
        'Grammatical accuracy and language range and control of register are still developing; however, cohesion '
        'remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while control of register meets the expected '
        'standard. Grammatical accuracy and language range are still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('strong', 'needs_work', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context. Grammatical accuracy and language range are '
        'still developing; however, cohesion remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. Grammatical accuracy and language range are still developing; however, '
        'cohesion remains less established and requires further development.'
    ),

    ('strong', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation, while grammatical accuracy and language range meet '
        'the expected standard. However, cohesion and control of register remain less established and require '
        'further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in organisation, while grammatical accuracy and language range meet '
        'the expected standard. Control of register is still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly, while '
        'grammatical accuracy and language range and control of register meet the expected standard. However, '
        'cohesion remains less established and is the main area requiring further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context, while grammatical accuracy and language range '
        'meet the expected standard. However, cohesion remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while grammatical accuracy and language range meet the expected standard. '
        'However, cohesion remains less established and requires further development.'
    ),

    ('strong', 'needs_work', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in grammatical '
        'accuracy and language range. However, cohesion and control of register remain less established and '
        'require further development.'
    ),
    ('strong', 'needs_work', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in grammatical '
        'accuracy and language range. Control of register is still developing; however, cohesion remains less '
        'established and requires further development.'
    ),
    ('strong', 'needs_work', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in grammatical '
        'accuracy and language range, while control of register meets the expected standard. However, cohesion '
        'remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in grammatical '
        'accuracy and language range and in adapting tone and style appropriately. However, cohesion remains '
        'less established and requires further development.'
    ),
    ('strong', 'needs_work', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in grammatical accuracy and language '
        'range. However, cohesion remains less established and requires further development.'
    ),

    ('strong', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range. '
        'However, cohesion and control of register remain less established and require further development.'
    ),
    ('strong', 'needs_work', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range. '
        'Control of register is still developing; however, cohesion remains less established and requires further '
        'development.'
    ),
    ('strong', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while control of register meets the expected standard. However, cohesion remains less established and '
        'requires further development.'
    ),
    ('strong', 'needs_work', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range and '
        'also demonstrates confidence in adapting tone and style appropriately to purpose, audience and context. '
        'However, cohesion remains less established and requires further development.'
    ),
    ('strong', 'needs_work', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, cohesion remains '
        'less established and is the main area requiring further development.'
    ),
    ('strong', 'developing', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly, while '
        'cohesion is still developing. However, grammatical accuracy and language range and control of register '
        'remain less established and require further development.'
    ),
    ('strong', 'developing', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in organisation. Cohesion and control of register are still '
        'developing; however, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while control of register meets the expected '
        'standard and cohesion is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('strong', 'developing', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context. Cohesion is still developing; however, '
        'grammatical accuracy and language range remain less established and require further development.'
    ),
    ('strong', 'developing', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. Cohesion is still developing; however, grammatical accuracy and language '
        'range remain less established and require further development.'
    ),

    ('strong', 'developing', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation, while cohesion and grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('strong', 'developing', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly. Cohesion, '
        'grammatical accuracy and language range, and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while control of register meets the expected '
        'standard. Cohesion and grammatical accuracy and language range are still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'developing', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context. Cohesion and grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context. However, cohesion and grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),

    ('strong', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation, while grammatical accuracy and language range meet '
        'the expected standard and cohesion is still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('strong', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in organisation, while grammatical accuracy and language range meet '
        'the expected standard. Cohesion and control of register are still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while grammatical accuracy and language range and '
        'control of register meet the expected standard. Cohesion is still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context. Grammatical accuracy and language range meet '
        'the expected standard, while cohesion is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while grammatical accuracy and language range meet the expected standard. '
        'Cohesion is still developing and would benefit from further consolidation.'
    ),

    ('strong', 'developing', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in grammatical '
        'accuracy and language range, while cohesion is still developing. However, control of register remains '
        'less established and requires further development.'
    ),
    ('strong', 'developing', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in grammatical '
        'accuracy and language range. Cohesion and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in grammatical '
        'accuracy and language range, while control of register meets the expected standard. Cohesion is still '
        'developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in grammatical '
        'accuracy and language range and in adapting tone and style appropriately. However, cohesion is still '
        'developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in grammatical accuracy and language '
        'range. Cohesion is still developing and would benefit from further consolidation.'
    ),

    ('strong', 'developing', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while cohesion is still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('strong', 'developing', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range. '
        'Cohesion and control of register are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while control of register meets the expected standard. Cohesion is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'developing', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range and '
        'also demonstrates confidence in adapting tone and style appropriately to purpose, audience and context. '
        'Cohesion is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'developing', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. However, cohesion is '
        'still developing and remains the principal area for further consolidation.'
    ),

    ('strong', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly, while '
        'cohesion meets the expected standard. However, grammatical accuracy and language range and control of '
        'register remain less established and require further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in organisation, while cohesion meets the expected standard and '
        'control of register is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while cohesion and control of register meet the '
        'expected standard. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context, while cohesion meets the expected standard. '
        'However, grammatical accuracy and language range remain less established and require further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while cohesion meets the expected standard. However, grammatical accuracy '
        'and language range remain less established and require further development.'
    ),

    ('strong', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation, while cohesion meets the expected standard and '
        'grammatical accuracy and language range are still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('strong', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in organisation, while cohesion meets the expected standard. '
        'Grammatical accuracy and language range and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation, while cohesion and control of register meet the '
        'expected standard. Grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'satisfactory', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context, while cohesion meets the expected standard. '
        'Grammatical accuracy and language range are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while cohesion meets the expected standard. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),

    ('strong', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation, while cohesion and grammatical accuracy and '
        'language range meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in organisation, while cohesion and grammatical accuracy and '
        'language range meet the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly, while '
        'cohesion, grammatical accuracy and language range, and control of register meet the expected standard, '
        'with further scope for development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in adapting tone '
        'and style appropriately to purpose, audience and context, while cohesion and grammatical accuracy and '
        'language range meet the expected standard.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while cohesion and grammatical accuracy and language range meet the '
        'expected standard, with further scope for development.'
    ),

    ('strong', 'satisfactory', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in grammatical '
        'accuracy and language range, while cohesion meets the expected standard. However, control of register '
        'remains less established and requires further development.'
    ),
    ('strong', 'satisfactory', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in grammatical '
        'accuracy and language range, while cohesion meets the expected standard. Control of register is still '
        'developing and would benefit from further consolidation.'
    ),
    ('strong', 'satisfactory', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in grammatical '
        'accuracy and language range, while cohesion and control of register meet the expected standard.'
    ),
    ('strong', 'satisfactory', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in grammatical '
        'accuracy and language range and in adapting tone and style appropriately, while cohesion meets the '
        'expected standard.'
    ),
    ('strong', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in grammatical accuracy and language '
        'range. Cohesion meets the expected standard, with further scope for development.'
    ),

    ('strong', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while cohesion meets the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('strong', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while cohesion meets the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while cohesion and control of register meet the expected standard, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range and '
        'also demonstrates confidence in adapting tone and style appropriately to purpose, audience and context. '
        'Cohesion meets the expected standard, with further scope for development.'
    ),
    ('strong', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context. Cohesion meets the '
        'expected standard, with further scope to develop greater consistency and sophistication.'
    ),

    ('strong', 'confident', 'needs_work', 'needs_work'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly and also '
        'demonstrates confidence in cohesion. However, grammatical accuracy and language range and control of '
        'register remain less established and require further development.'
    ),
    ('strong', 'confident', 'needs_work', 'developing'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'control of register is still developing. However, grammatical accuracy and language range remain less '
        'established and require further development.'
    ),
    ('strong', 'confident', 'needs_work', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'control of register meets the expected standard. However, grammatical accuracy and language range remain '
        'less established and require further development.'
    ),
    ('strong', 'confident', 'needs_work', 'confident'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in cohesion and in '
        'adapting tone and style appropriately to purpose, audience and context. However, grammatical accuracy '
        'and language range remain less established and require further development.'
    ),
    ('strong', 'confident', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in cohesion. However, grammatical '
        'accuracy and language range remain less established and require further development.'
    ),

    ('strong', 'confident', 'developing', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'grammatical accuracy and language range are still developing. However, control of register remains less '
        'established and requires further development.'
    ),
    ('strong', 'confident', 'developing', 'developing'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion. '
        'Grammatical accuracy and language range and control of register are still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'confident', 'developing', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'control of register meets the expected standard. Grammatical accuracy and language range are still '
        'developing and would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'developing', 'confident'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in cohesion and in '
        'adapting tone and style appropriately to purpose, audience and context. Grammatical accuracy and language '
        'range are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in cohesion. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),

    ('strong', 'confident', 'satisfactory', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'grammatical accuracy and language range meet the expected standard. However, control of register remains '
        'less established and requires further development.'
    ),
    ('strong', 'confident', 'satisfactory', 'developing'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'grammatical accuracy and language range meet the expected standard. Control of register is still '
        'developing and would benefit from further consolidation.'
    ),
    ('strong', 'confident', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and also demonstrates confidence in cohesion, while '
        'grammatical accuracy and language range and control of register meet the expected standard, with further '
        'scope for development.'
    ),
    ('strong', 'confident', 'satisfactory', 'confident'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in cohesion and in '
        'adapting tone and style appropriately to purpose, audience and context, while grammatical accuracy and '
        'language range meet the expected standard.'
    ),
    ('strong', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in cohesion. Grammatical accuracy and '
        'language range meet the expected standard, with further scope for development.'
    ),

    ('strong', 'confident', 'confident', 'needs_work'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in cohesion and in '
        'grammatical accuracy and language range. However, control of register remains less established and '
        'requires further development.'
    ),
    ('strong', 'confident', 'confident', 'developing'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in cohesion and in '
        'grammatical accuracy and language range. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'confident', 'confident', 'satisfactory'): (
        '{learner_name} shows a clear strength in organisation and demonstrates confidence in cohesion and in '
        'grammatical accuracy and language range, while control of register meets the expected standard.'
    ),
    ('strong', 'confident', 'confident', 'confident'): (
        '{learner_name} shows a clear strength in organising written work and presenting ideas clearly, while '
        'demonstrating confidence in cohesion, grammatical accuracy and language range, and the ability to adapt '
        'tone and style appropriately to purpose, audience and context.'
    ),
    ('strong', 'confident', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in organisation and in adapting tone and style appropriately to '
        'purpose, audience and context, while also demonstrating confidence in cohesion and in grammatical '
        'accuracy and language range.'
    ),

    ('strong', 'confident', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range and '
        'also demonstrates confidence in cohesion. However, control of register remains less established and '
        'requires further development.'
    ),
    ('strong', 'confident', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range and '
        'also demonstrates confidence in cohesion. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while also demonstrating confidence in cohesion. Control of register meets the expected standard, with '
        'further scope for development.'
    ),
    ('strong', 'confident', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in organisation and in grammatical accuracy and language range, '
        'while also demonstrating confidence in cohesion and in adapting tone and style appropriately to purpose, '
        'audience and context.'
    ),
    ('strong', 'confident', 'strong', 'strong'): (
        '{learner_name} shows clear strengths in organisation, grammatical accuracy and language range, and the '
        'ability to adapt tone and style appropriately to purpose, audience and context, while also demonstrating '
        'confidence in connecting ideas logically and maintaining coherence.'
    ),

    ('strong', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and cohesion. However, grammatical accuracy and '
        'language range and control of register remain less established and require further development.'
    ),
    ('strong', 'strong', 'needs_work', 'developing'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while control of register is still '
        'developing. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while control of register meets the '
        'expected standard. However, grammatical accuracy and language range remain less established and require '
        'further development.'
    ),
    ('strong', 'strong', 'needs_work', 'confident'): (
        '{learner_name} shows clear strengths in organisation and cohesion and also demonstrates confidence in '
        'adapting tone and style appropriately to purpose, audience and context. However, grammatical accuracy '
        'and language range remain less established and require further development.'
    ),
    ('strong', 'strong', 'needs_work', 'strong'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context. However, grammatical accuracy and language range remain '
        'less established and are the main area requiring further development.'
    ),

    ('strong', 'strong', 'developing', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while grammatical accuracy and '
        'language range are still developing. However, control of register remains less established and requires '
        'further development.'
    ),
    ('strong', 'strong', 'developing', 'developing'): (
        '{learner_name} shows clear strengths in organisation and cohesion. Grammatical accuracy and language '
        'range and control of register are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while control of register meets the '
        'expected standard. Grammatical accuracy and language range are still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'strong', 'developing', 'confident'): (
        '{learner_name} shows clear strengths in organisation and cohesion and also demonstrates confidence in '
        'adapting tone and style appropriately to purpose, audience and context. Grammatical accuracy and '
        'language range are still developing and would benefit from further consolidation.'
    ),
    ('strong', 'strong', 'developing', 'strong'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context. However, grammatical accuracy and language range are '
        'still developing and would benefit from further consolidation.'
    ),

    ('strong', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while grammatical accuracy and '
        'language range meet the expected standard. However, control of register remains less established and '
        'requires further development.'
    ),
    ('strong', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while grammatical accuracy and '
        'language range meet the expected standard. Control of register is still developing and would benefit '
        'from further consolidation.'
    ),
    ('strong', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while grammatical accuracy and '
        'language range and control of register meet the expected standard, with further scope for development.'
    ),
    ('strong', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} shows clear strengths in organisation and cohesion and also demonstrates confidence in '
        'adapting tone and style appropriately to purpose, audience and context, while grammatical accuracy and '
        'language range meet the expected standard.'
    ),
    ('strong', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context, while grammatical accuracy and language range meet the '
        'expected standard, with further scope for development.'
    ),

    ('strong', 'strong', 'confident', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation and cohesion and also demonstrates confidence in '
        'grammatical accuracy and language range. However, control of register remains less established and '
        'requires further development.'
    ),
    ('strong', 'strong', 'confident', 'developing'): (
        '{learner_name} shows clear strengths in organisation and cohesion and also demonstrates confidence in '
        'grammatical accuracy and language range. Control of register is still developing and would benefit from '
        'further consolidation.'
    ),
    ('strong', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation and cohesion and demonstrates confidence in '
        'grammatical accuracy and language range, while control of register meets the expected standard.'
    ),
    ('strong', 'strong', 'confident', 'confident'): (
        '{learner_name} shows clear strengths in organisation and cohesion, while also demonstrating confidence '
        'in grammatical accuracy and language range and in adapting tone and style appropriately to purpose, '
        'audience and context.'
    ),
    ('strong', 'strong', 'confident', 'strong'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and the ability to adapt tone and style '
        'appropriately to purpose, audience and context, while also demonstrating confidence in grammatical '
        'accuracy and language range.'
    ),

    ('strong', 'strong', 'strong', 'needs_work'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and grammatical accuracy and language '
        'range. However, control of register remains less established and is the main area requiring further '
        'development.'
    ),
    ('strong', 'strong', 'strong', 'developing'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and grammatical accuracy and language '
        'range. Control of register is still developing and would benefit from further consolidation.'
    ),
    ('strong', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and grammatical accuracy and language '
        'range, while control of register meets the expected standard, with further scope for development.'
    ),
    ('strong', 'strong', 'strong', 'confident'): (
        '{learner_name} shows clear strengths in organisation, cohesion, and grammatical accuracy and language '
        'range and also demonstrates confidence in adapting tone and style appropriately to purpose, audience '
        'and context.'
    ),
    ('strong', 'strong', 'strong', 'strong'): (
        'Written communication is a clear strength for {learner_name}, who demonstrates consistently strong '
        'performance across organisation and clarity, cohesion, grammatical accuracy and language range, and '
        'control of register.'
    ),
}
