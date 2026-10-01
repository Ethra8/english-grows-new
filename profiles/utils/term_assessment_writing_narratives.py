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
        "{learner_name}'s written communication falls well below the minimum expected "
        'standard for this level across all four assessed areas. Organising and '
        'presenting written work clearly, connecting ideas logically and maintaining '
        'coherence, grammatical accuracy and language range, and adapting tone and '
        'style appropriately to purpose, audience and context all require substantial '
        'further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, the three assessed areas, '
        'namely organisation and clear presentation of written work, connecting ideas '
        'logically and maintaining coherence, and grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context satisfactorily meets the minimum expected standard for this level. '
        'However, the three assessed areas, namely organisation and clear presentation '
        'of written work, connecting ideas logically and maintaining coherence, and '
        'grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established. However, the three assessed areas, namely '
        'organisation and clear presentation of written work, connecting ideas '
        'logically and maintaining coherence, and grammatical accuracy and language '
        'range, fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong. However, the three assessed areas, namely '
        'organisation and clear presentation of written work, connecting ideas '
        'logically and maintaining coherence, and grammatical accuracy and language '
        'range, fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are still developing "
        'and require further consolidation to reach the minimum expected standard for '
        'this level. However, the three assessed areas, namely organisation and clear '
        'presentation of written work, connecting ideas logically and maintaining '
        'coherence, and adapting tone and style to purpose, audience and context, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s performance is still developing in grammatical accuracy and "
        'language range, as well as in appropriate tone and style and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the two assessed areas, namely organisation and clear presentation of written '
        'work, as well as connecting ideas logically and maintaining coherence, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context satisfactorily meets the minimum expected standard for this level. '
        'Grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'connecting ideas logically and maintaining coherence, fall well below that '
        'standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established. Grammatical accuracy and language range are '
        'still developing and require further consolidation to reach the minimum '
        'expected standard for this level. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as connecting '
        'ideas logically and maintaining coherence, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong. Grammatical accuracy and language range are '
        'still developing and require further consolidation to reach the minimum '
        'expected standard for this level. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as connecting '
        'ideas logically and maintaining coherence, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. However, the three assessed '
        'areas, namely organisation and clear presentation of written work, connecting '
        'ideas logically and maintaining coherence, and adapting tone and style to '
        'purpose, audience and context, fall well below that standard and require '
        'substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. The ability to adapt tone and '
        'style to purpose, audience and context is still developing and requires '
        'further consolidation to reach that standard. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'connecting ideas logically and maintaining coherence, fall well below that '
        'standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in grammatical accuracy and language range, as well as in appropriate '
        'tone and style. However, the two assessed areas, namely organisation and '
        'clear presentation of written work, as well as connecting ideas logically and '
        'maintaining coherence, fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the two assessed areas, namely organisation and clear presentation of written '
        'work, as well as connecting ideas logically and maintaining coherence, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the two assessed areas, namely organisation and clear presentation of written '
        'work, as well as connecting ideas logically and maintaining coherence, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. However, the three assessed areas, namely organisation and clear '
        'presentation of written work, connecting ideas logically and maintaining '
        'coherence, and adapting tone and style to purpose, audience and context, fall '
        'well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The ability to adapt tone and style to purpose, audience and '
        'context is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, the two assessed areas, '
        'namely organisation and clear presentation of written work, as well as '
        'connecting ideas logically and maintaining coherence, fall well below that '
        'standard and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established, while the ability to adapt tone and style to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this '
        'level. However, the two assessed areas, namely organisation and clear '
        'presentation of written work, as well as connecting ideas logically and '
        'maintaining coherence, fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in grammatical accuracy and "
        'language range, as well as in appropriate tone and style, with confidence '
        'evident in both areas. However, the two assessed areas, namely organisation '
        'and clear presentation of written work, as well as connecting ideas logically '
        'and maintaining coherence, fall well below the minimum expected standard for '
        'this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while grammatical accuracy and language range '
        'are also well established. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as connecting '
        'ideas logically and maintaining coherence, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. However, the three assessed areas, namely organisation and clear '
        'presentation of written work, connecting ideas logically and maintaining '
        'coherence, and adapting tone and style to purpose, audience and context, fall '
        'well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to adapt tone and style to purpose, audience and context '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as connecting '
        'ideas logically and maintaining coherence, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level. '
        'However, the two assessed areas, namely organisation and clear presentation '
        'of written work, as well as connecting ideas logically and maintaining '
        'coherence, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style to purpose, audience and '
        'context is also well established. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as connecting '
        'ideas logically and maintaining coherence, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'needs_work', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range, as well as in appropriate tone and style. However, the two '
        'assessed areas, namely organisation and clear presentation of written work, '
        'as well as connecting ideas logically and maintaining coherence, fall well '
        'below the minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the three assessed areas, namely '
        'organisation and clear presentation of written work, grammatical accuracy and '
        'language range, and adapting tone and style to purpose, audience and context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s performance is still developing in cohesion and logical "
        'connection of ideas, as well as in appropriate tone and style and requires '
        'further consolidation to reach the minimum expected standard for this level. '
        'However, the two assessed areas, namely organisation and clear presentation '
        'of written work, as well as grammatical accuracy and language range, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context satisfactorily meets the minimum expected standard for this level. '
        'The ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the two assessed areas, namely organisation and clear presentation '
        'of written work, as well as grammatical accuracy and language range, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established. The ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong. The ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s performance is still developing in cohesion and logical "
        'connection of ideas, as well as in grammatical accuracy and language range '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, the two assessed areas, namely organisation and clear '
        'presentation of written work, as well as adapting tone and style to purpose, '
        'audience and context, fall well below that standard and require substantial '
        'further development.'
    ),
    ('needs_work', 'developing', 'developing', 'developing'): (
        "{learner_name}'s performance is still developing in cohesion and logical "
        'connection of ideas, in grammatical accuracy and language range, and in '
        'appropriate tone and style and requires further consolidation to reach the '
        'minimum expected standard for this level. However, the ability to organise '
        'and present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context satisfactorily meets the minimum expected standard for this level. '
        'Performance is still developing in cohesion and logical connection of ideas, '
        'as well as in grammatical accuracy and language range and requires further '
        'consolidation to reach that standard. However, the ability to organise and '
        'present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established. Performance is still developing in cohesion and '
        'logical connection of ideas, as well as in grammatical accuracy and language '
        'range and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'developing', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong. Performance is still developing in cohesion '
        'and logical connection of ideas, as well as in grammatical accuracy and '
        'language range and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to organise and '
        'present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. The ability to connect ideas '
        'logically and maintain coherence is still developing and requires further '
        'consolidation to reach that standard. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as adapting tone '
        'and style to purpose, audience and context, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. Performance is still developing '
        'in cohesion and logical connection of ideas, as well as in appropriate tone '
        'and style and requires further consolidation to reach that standard. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in grammatical accuracy and language range, as well as in appropriate '
        'tone and style. The ability to connect ideas logically and maintain coherence '
        'is still developing and requires further consolidation to reach that '
        'standard. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. The ability '
        'to connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach that standard. However, the ability '
        'to organise and present written work clearly falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. The ability '
        'to connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach that standard. However, the ability '
        'to organise and present written work clearly falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The ability to connect ideas logically and maintain coherence is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as adapting tone '
        'and style to purpose, audience and context, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. Performance is still developing in cohesion and logical '
        'connection of ideas, as well as in appropriate tone and style and requires '
        'further consolidation to reach the minimum expected standard for this level. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established, while the ability to adapt tone and style to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this '
        'level. The ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in grammatical accuracy and "
        'language range, as well as in appropriate tone and style, with confidence '
        'evident in both areas. The ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, the ability to organise '
        'and present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'developing', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while grammatical accuracy and language range '
        'are also well established. The ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to connect ideas logically and maintain coherence is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as adapting tone '
        'and style to purpose, audience and context, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Performance is still developing in cohesion and logical connection of '
        'ideas, as well as in appropriate tone and style and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level. '
        'The ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style to purpose, audience and '
        'context is also well established. The ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'developing', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range, as well as in appropriate tone and style. The ability to '
        'connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach the minimum expected standard for '
        'this level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the three assessed areas, namely organisation and clear presentation of '
        'written work, grammatical accuracy and language range, and adapting tone and '
        'style to purpose, audience and context, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to adapt tone and style to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the two assessed areas, namely organisation and clear presentation '
        'of written work, as well as grammatical accuracy and language range, fall '
        'well below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in cohesion and logical connection of ideas, as well as in appropriate '
        'tone and style. However, the two assessed areas, namely organisation and '
        'clear presentation of written work, as well as grammatical accuracy and '
        'language range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established, while the ability to connect ideas logically and '
        'maintain coherence satisfactorily meets the minimum expected standard for '
        'this level. However, the two assessed areas, namely organisation and clear '
        'presentation of written work, as well as grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while the ability to connect ideas logically '
        'and maintain coherence satisfactorily meets the minimum expected standard for '
        'this level. However, the two assessed areas, namely organisation and clear '
        'presentation of written work, as well as grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. '
        'Grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'adapting tone and style to purpose, audience and context, fall well below '
        'that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. '
        'Performance is still developing in grammatical accuracy and language range, '
        'as well as in appropriate tone and style and requires further consolidation '
        'to reach that standard. However, the ability to organise and present written '
        'work clearly falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in cohesion and logical connection of ideas, as well as in appropriate '
        'tone and style. Grammatical accuracy and language range are still developing '
        'and require further consolidation to reach that standard. However, the '
        'ability to organise and present written work clearly falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established, while the ability to connect ideas logically and '
        'maintain coherence satisfactorily meets the minimum expected standard for '
        'this level. Grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while the ability to connect ideas logically '
        'and maintain coherence satisfactorily meets the minimum expected standard for '
        'this level. Grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in cohesion and logical connection of ideas, as well as in grammatical '
        'accuracy and language range. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as adapting tone '
        'and style to purpose, audience and context, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in cohesion and logical connection of ideas, as well as in grammatical '
        'accuracy and language range. The ability to adapt tone and style to purpose, '
        'audience and context is still developing and requires further consolidation '
        'to reach that standard. However, the ability to organise and present written '
        'work clearly falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in cohesion and logical connection of ideas, in grammatical accuracy '
        'and language range, and in appropriate tone and style. However, the ability '
        'to organise and present written work clearly falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is well established. The learner satisfactorily meets the minimum '
        'expected standard for this level in cohesion and logical connection of ideas, '
        'as well as in grammatical accuracy and language range. However, the ability '
        'to organise and present written work clearly falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong. The learner satisfactorily meets the minimum '
        'expected standard for this level in cohesion and logical connection of ideas, '
        'as well as in grammatical accuracy and language range. However, the ability '
        'to organise and present written work clearly falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established, while the ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'However, the two assessed areas, namely organisation and clear presentation '
        'of written work, as well as adapting tone and style to purpose, audience and '
        'context, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established, while the ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'The ability to adapt tone and style to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The learner satisfactorily meets the minimum expected standard '
        'for this level in cohesion and logical connection of ideas, as well as in '
        'appropriate tone and style. However, the ability to organise and present '
        'written work clearly falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in grammatical accuracy and "
        'language range, as well as in appropriate tone and style, with confidence '
        'evident in both areas. The ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while grammatical accuracy and language range '
        'are also well established. The ability to connect ideas logically and '
        'maintain coherence satisfactorily meets the minimum expected standard for '
        'this level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the two assessed areas, namely organisation and clear presentation of written '
        'work, as well as adapting tone and style to purpose, audience and context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to adapt tone and style to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The learner satisfactorily meets the minimum expected standard for '
        'this level in cohesion and logical connection of ideas, as well as in '
        'appropriate tone and style. However, the ability to organise and present '
        'written work clearly falls well below that standard and requires substantial '
        'further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style to purpose, audience and '
        'context is also well established. The ability to connect ideas logically and '
        'maintain coherence satisfactorily meets the minimum expected standard for '
        'this level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range, as well as in appropriate tone and style. The ability to '
        'connect ideas logically and maintain coherence satisfactorily meets the '
        'minimum expected standard for this level. However, the ability to organise '
        'and present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. However, the three assessed areas, namely organisation and '
        'clear presentation of written work, grammatical accuracy and language range, '
        'and adapting tone and style to purpose, audience and context, fall well below '
        'the minimum expected standard for this level and require substantial further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. The ability to adapt tone and style to purpose, audience '
        'and context is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while the ability to adapt tone and style to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, the two assessed areas, namely organisation and clear '
        'presentation of written work, as well as grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, as well as in appropriate tone and style, with '
        'confidence evident in both areas. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as grammatical '
        'accuracy and language range, fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while the ability to connect ideas logically '
        'and maintain coherence is also well established. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'grammatical accuracy and language range, fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. Grammatical accuracy and language range are still '
        'developing and require further consolidation to reach the minimum expected '
        'standard for this level. However, the two assessed areas, namely organisation '
        'and clear presentation of written work, as well as adapting tone and style to '
        'purpose, audience and context, fall well below that standard and require '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. Performance is still developing in grammatical accuracy and '
        'language range, as well as in appropriate tone and style and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while the ability to adapt tone and style to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. Grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'confident', 'developing', 'confident'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, as well as in appropriate tone and style, with '
        'confidence evident in both areas. Grammatical accuracy and language range are '
        'still developing and require further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to organise and '
        'present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while the ability to connect ideas logically '
        'and maintain coherence is also well established. Grammatical accuracy and '
        'language range are still developing and require further consolidation to '
        'reach the minimum expected standard for this level. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the two assessed areas, namely organisation and clear presentation of written '
        'work, as well as adapting tone and style to purpose, audience and context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. The ability '
        'to adapt tone and style to purpose, audience and context is still developing '
        'and requires further consolidation to reach that standard. However, the '
        'ability to organise and present written work clearly falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. The learner satisfactorily meets the minimum expected '
        'standard for this level in grammatical accuracy and language range, as well '
        'as in appropriate tone and style. However, the ability to organise and '
        'present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, as well as in appropriate tone and style, with '
        'confidence evident in both areas. Grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong, while the ability to connect ideas logically '
        'and maintain coherence is also well established. Grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this '
        'level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, as well as in grammatical accuracy and language range, '
        'with confidence evident in both areas. However, the two assessed areas, '
        'namely organisation and clear presentation of written work, as well as '
        'adapting tone and style to purpose, audience and context, fall well below the '
        'minimum expected standard for this level and require substantial further '
        'development.'
    ),
    ('needs_work', 'confident', 'confident', 'developing'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, as well as in grammatical accuracy and language range, '
        'with confidence evident in both areas. The ability to adapt tone and style to '
        'purpose, audience and context is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, as well as in grammatical accuracy and language range, '
        'with confidence evident in both areas. The ability to adapt tone and style to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'confident', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in cohesion and logical "
        'connection of ideas, in grammatical accuracy and language range, and in '
        'appropriate tone and style, with confidence evident in all three areas. '
        'However, the ability to organise and present written work clearly falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('needs_work', 'confident', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style to purpose, audience and "
        'context is particularly strong. Performance is well established in cohesion '
        'and logical connection of ideas, as well as in grammatical accuracy and '
        'language range, with confidence evident in both areas. However, the ability '
        'to organise and present written work clearly falls well below the minimum '
        'expected standard for this level and requires substantial further '
        'development.'
    ),
    ('needs_work', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'is also well established. However, the two assessed areas, namely '
        'organisation and clear presentation of written work, as well as adapting tone '
        'and style to purpose, audience and context, fall well below the minimum '
        'expected standard for this level and require substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'is also well established. The ability to adapt tone and style to purpose, '
        'audience and context is still developing and requires further consolidation '
        'to reach the minimum expected standard for this level. However, the ability '
        'to organise and present written work clearly falls well below that standard '
        'and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'is also well established. The ability to adapt tone and style to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Performance is well established in cohesion and logical connection of '
        'ideas, as well as in appropriate tone and style, with confidence evident in '
        'both areas. However, the ability to organise and present written work clearly '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('needs_work', 'confident', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range, as well as in appropriate tone and style. The ability to '
        'connect ideas logically and maintain coherence is well established. However, '
        'the ability to organise and present written work clearly falls well below the '
        'minimum expected standard for this level and requires substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. However, the three assessed areas, namely organisation '
        'and clear presentation of written work, grammatical accuracy and language '
        'range, and adapting tone and style to purpose, audience and context, fall '
        'well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to adapt tone and style to purpose, audience '
        'and context is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, the two assessed areas, namely organisation and clear '
        'presentation of written work, as well as grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style to purpose, '
        'audience and context is also well established. However, the two assessed '
        'areas, namely organisation and clear presentation of written work, as well as '
        'grammatical accuracy and language range, fall well below the minimum expected '
        'standard for this level and require substantial further development.'
    ),
    ('needs_work', 'strong', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in appropriate tone and style. However, the '
        'two assessed areas, namely organisation and clear presentation of written '
        'work, as well as grammatical accuracy and language range, fall well below the '
        'minimum expected standard for this level and require substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Grammatical accuracy and language range are still '
        'developing and require further consolidation to reach the minimum expected '
        'standard for this level. However, the two assessed areas, namely organisation '
        'and clear presentation of written work, as well as adapting tone and style to '
        'purpose, audience and context, fall well below that standard and require '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is still developing in grammatical accuracy '
        'and language range, as well as in appropriate tone and style and requires '
        'further consolidation to reach the minimum expected standard for this level. '
        'However, the ability to organise and present written work clearly falls well '
        'below that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. Grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style to purpose, '
        'audience and context is also well established. Grammatical accuracy and '
        'language range are still developing and require further consolidation to '
        'reach the minimum expected standard for this level. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'strong', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in appropriate tone and style. Grammatical '
        'accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the two assessed areas, namely organisation and clear presentation of written '
        'work, as well as adapting tone and style to purpose, audience and context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. The ability '
        'to adapt tone and style to purpose, audience and context is still developing '
        'and requires further consolidation to reach that standard. However, the '
        'ability to organise and present written work clearly falls well below that '
        'standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The learner satisfactorily meets the minimum expected '
        'standard for this level in grammatical accuracy and language range, as well '
        'as in appropriate tone and style. However, the ability to organise and '
        'present written work clearly falls well below that standard and requires '
        'substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style to purpose, '
        'audience and context is also well established. Grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this '
        'level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in appropriate tone and style. Grammatical '
        'accuracy and language range satisfactorily meet the minimum expected standard '
        'for this level. However, the ability to organise and present written work '
        'clearly falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range are also '
        'well established. However, the two assessed areas, namely organisation and '
        'clear presentation of written work, as well as adapting tone and style to '
        'purpose, audience and context, fall well below the minimum expected standard '
        'for this level and require substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range are also '
        'well established. The ability to adapt tone and style to purpose, audience '
        'and context is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level. However, the ability to '
        'organise and present written work clearly falls well below that standard and '
        'requires substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range are also '
        'well established. The ability to adapt tone and style to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this '
        'level. However, the ability to organise and present written work clearly '
        'falls well below that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is well established in grammatical accuracy '
        'and language range, as well as in appropriate tone and style, with confidence '
        'evident in both areas. However, the ability to organise and present written '
        'work clearly falls well below the minimum expected standard for this level '
        'and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in appropriate tone and style. Grammatical '
        'accuracy and language range are well established. However, the ability to '
        'organise and present written work clearly falls well below the minimum '
        'expected standard for this level and requires substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in grammatical accuracy and language range. '
        'However, the two assessed areas, namely organisation and clear presentation '
        'of written work, as well as adapting tone and style to purpose, audience and '
        'context, fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in grammatical accuracy and language range. '
        'The ability to adapt tone and style to purpose, audience and context is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly falls well below that standard and requires substantial further '
        'development.'
    ),
    ('needs_work', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in grammatical accuracy and language range. '
        'The ability to adapt tone and style to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly falls well below '
        'that standard and requires substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, as well as in grammatical accuracy and language range. '
        'The ability to adapt tone and style to purpose, audience and context is well '
        'established. However, the ability to organise and present written work '
        'clearly falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('needs_work', 'strong', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in cohesion and logical '
        'connection of ideas, in grammatical accuracy and language range, and in '
        'appropriate tone and style. However, the ability to organise and present '
        'written work clearly falls well below the minimum expected standard for this '
        'level and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is still "
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the remaining three assessed areas, namely '
        'connecting ideas logically and maintaining coherence, grammatical accuracy and '
        'language range, and adapting tone and style appropriately to purpose, audience '
        'and context, fall well below that standard and require substantial further '
        'development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s performance is still developing in organising and presenting "
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the remaining two assessed areas, '
        'namely connecting ideas logically and maintaining coherence and grammatical '
        'accuracy and language range, fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. The ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard. However, '
        'the remaining two assessed areas, namely connecting ideas logically and '
        'maintaining coherence and grammatical accuracy and language range, fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. The ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the remaining two '
        'assessed areas, namely connecting ideas logically and maintaining coherence '
        'and grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('developing', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. The ability to organise and '
        'present written work clearly is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the remaining two assessed areas, namely connecting ideas logically and '
        'maintaining coherence and grammatical accuracy and language range, fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s performance is still developing in organising and presenting "
        'written work clearly and in grammatical accuracy and language range and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the remaining two assessed areas, namely connecting ideas '
        'logically and maintaining coherence and adapting tone and style appropriately '
        'to purpose, audience and context, fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s performance is still developing in organising and presenting "
        'written work clearly, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the ability to connect ideas logically and maintain coherence '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. Performance is still developing in organising and presenting '
        'written work clearly and in grammatical accuracy and language range and '
        'requires further consolidation to reach that standard. However, the ability to '
        'connect ideas logically and maintain coherence falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Performance is still developing in '
        'organising and presenting written work clearly and in grammatical accuracy and '
        'language range and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Performance is still developing '
        'in organising and presenting written work clearly and in grammatical accuracy '
        'and language range and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. The ability to organise and '
        'present written work clearly is still developing and requires further '
        'consolidation to reach that standard. However, the remaining two assessed '
        'areas, namely connecting ideas logically and maintaining coherence and '
        'adapting tone and style appropriately to purpose, audience and context, fall '
        'well below that standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. Performance is still developing '
        'in organising and presenting written work clearly and in adapting tone and '
        'style appropriately to purpose, audience and context and requires further '
        'consolidation to reach that standard. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. The ability to organise '
        'and present written work clearly is still developing and requires further '
        'consolidation to reach that standard. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established, while grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this '
        'level. The ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard. However, '
        'the ability to connect ideas logically and maintain coherence falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this '
        'level. The ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard. However, '
        'the ability to connect ideas logically and maintain coherence falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established. "
        'The ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, the remaining two assessed areas, namely connecting ideas '
        'logically and maintaining coherence and adapting tone and style appropriately '
        'to purpose, audience and context, fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established. "
        'Performance is still developing in organising and presenting written work '
        'clearly and in adapting tone and style appropriately to purpose, audience and '
        'context and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, "
        'while the ability to adapt tone and style appropriately to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this level. '
        'The ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach that standard. However, the '
        'ability to connect ideas logically and maintain coherence falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in grammatical accuracy and "
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident in both assessed areas. The '
        'ability to organise and present written work clearly is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the ability to connect ideas logically and maintain coherence '
        'falls well below that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while grammatical accuracy and '
        'language range are also well established. The ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the ability to '
        'connect ideas logically and maintain coherence falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the remaining two assessed areas, namely '
        'connecting ideas logically and maintaining coherence and adapting tone and '
        'style appropriately to purpose, audience and context, fall well below that '
        'standard and require substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Performance is still developing in organising and presenting written '
        'work clearly and in adapting tone and style appropriately to purpose, audience '
        'and context and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style appropriately to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. The ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard. However, '
        'the ability to connect ideas logically and maintain coherence falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style appropriately to purpose, '
        'audience and context is also well established. The ability to organise and '
        'present written work clearly is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'needs_work', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context. The ability to organise and present written work clearly '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s performance is still developing in organising and presenting "
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence and requires further consolidation to reach the minimum expected '
        'standard for this level. However, the remaining two assessed areas, namely '
        'grammatical accuracy and language range and adapting tone and style '
        'appropriately to purpose, audience and context, fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s performance is still developing in organising and presenting "
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in adapting tone and style appropriately to purpose, audience and context '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. Performance is still developing in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence and requires further consolidation to reach that standard. However, '
        'grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Performance is still developing in '
        'organising and presenting written work clearly and in connecting ideas '
        'logically and maintaining coherence and requires further consolidation to '
        'reach the minimum expected standard for this level. However, grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Performance is still developing '
        'in organising and presenting written work clearly and in connecting ideas '
        'logically and maintaining coherence and requires further consolidation to '
        'reach the minimum expected standard for this level. However, grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s performance is still developing in organising and presenting "
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in grammatical accuracy and language range and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'the ability to adapt tone and style appropriately to purpose, audience and '
        'context falls well below that standard and requires substantial further '
        'development.'
    ),
    ('developing', 'developing', 'developing', 'developing'): (
        "{learner_name}'s written communication is still developing across all four "
        'assessed areas. Organising and presenting written work clearly, connecting '
        'ideas logically and maintaining coherence, grammatical accuracy and language '
        'range, and adapting tone and style to purpose, audience and context have not '
        'yet reached the minimum expected standard for this level and require further '
        'consolidation.'
    ),
    ('developing', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, performance is still developing in organising and '
        'presenting written work clearly, in connecting ideas logically and maintaining '
        'coherence, and in grammatical accuracy and language range and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. However, performance is still '
        'developing in organising and presenting written work clearly, in connecting '
        'ideas logically and maintaining coherence, and in grammatical accuracy and '
        'language range and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'developing', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. However, performance is still '
        'developing in organising and presenting written work clearly, in connecting '
        'ideas logically and maintaining coherence, and in grammatical accuracy and '
        'language range and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. Performance is still developing '
        'in organising and presenting written work clearly and in connecting ideas '
        'logically and maintaining coherence and requires further consolidation to '
        'reach that standard. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range satisfactorily meet "
        'the minimum expected standard for this level. However, performance is still '
        'developing in organising and presenting written work clearly, in connecting '
        'ideas logically and maintaining coherence, and in adapting tone and style '
        'appropriately to purpose, audience and context and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in grammatical accuracy and language range and in adapting tone and '
        'style appropriately to purpose, audience and context. However, performance is '
        'still developing in organising and presenting written work clearly and in '
        'connecting ideas logically and maintaining coherence and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established, while grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this '
        'level. However, performance is still developing in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence and requires further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this '
        'level. However, performance is still developing in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence and requires further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established. "
        'Performance is still developing in organising and presenting written work '
        'clearly and in connecting ideas logically and maintaining coherence and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'developing', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established. "
        'However, performance is still developing in organising and presenting written '
        'work clearly, in connecting ideas logically and maintaining coherence, and in '
        'adapting tone and style appropriately to purpose, audience and context and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('developing', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established, "
        'while the ability to adapt tone and style appropriately to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this level. '
        'However, performance is still developing in organising and presenting written '
        'work clearly and in connecting ideas logically and maintaining coherence and '
        'requires further consolidation to reach that standard.'
    ),
    ('developing', 'developing', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in grammatical accuracy and "
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident in both assessed areas. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in connecting ideas logically and maintaining coherence and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('developing', 'developing', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while grammatical accuracy and '
        'language range are also well established. However, performance is still '
        'developing in organising and presenting written work clearly and in connecting '
        'ideas logically and maintaining coherence and requires further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Performance is still developing in organising and presenting written '
        'work clearly and in connecting ideas logically and maintaining coherence and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'developing', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. However, performance is still developing in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in adapting tone and style appropriately to purpose, audience and context '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('developing', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style appropriately to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, performance is still developing in organising and '
        'presenting written work clearly and in connecting ideas logically and '
        'maintaining coherence and requires further consolidation to reach that '
        'standard.'
    ),
    ('developing', 'developing', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style appropriately to purpose, '
        'audience and context is also well established. However, performance is still '
        'developing in organising and presenting written work clearly and in connecting '
        'ideas logically and maintaining coherence and requires further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('developing', 'developing', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context. However, performance is still developing in organising '
        'and presenting written work clearly and in connecting ideas logically and '
        'maintaining coherence and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. The ability '
        'to organise and present written work clearly is still developing and requires '
        'further consolidation to reach that standard. However, the remaining two '
        'assessed areas, namely grammatical accuracy and language range and adapting '
        'tone and style appropriately to purpose, audience and context, fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'is still developing in organising and presenting written work clearly and in '
        'adapting tone and style appropriately to purpose, audience and context and '
        'requires further consolidation to reach that standard. However, grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in connecting ideas logically and maintaining coherence and in adapting '
        'tone and style appropriately to purpose, audience and context. The ability to '
        'organise and present written work clearly is still developing and requires '
        'further consolidation to reach that standard. However, grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established, while the ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected '
        'standard for this level. The ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach that '
        'standard. However, grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to connect '
        'ideas logically and maintain coherence satisfactorily meets the minimum '
        'expected standard for this level. The ability to organise and present written '
        'work clearly is still developing and requires further consolidation to reach '
        'that standard. However, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'is still developing in organising and presenting written work clearly and in '
        'grammatical accuracy and language range and requires further consolidation to '
        'reach that standard. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance is still developing in organising and presenting written work '
        'clearly, in grammatical accuracy and language range, and in adapting tone and '
        'style appropriately to purpose, audience and context and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in connecting ideas logically and maintaining coherence and in adapting '
        'tone and style appropriately to purpose, audience and context. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in grammatical accuracy and language range and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established, while the ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected '
        'standard for this level. However, performance is still developing in '
        'organising and presenting written work clearly and in grammatical accuracy and '
        'language range and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to connect '
        'ideas logically and maintain coherence satisfactorily meets the minimum '
        'expected standard for this level. However, performance is still developing in '
        'organising and presenting written work clearly and in grammatical accuracy and '
        'language range and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in connecting ideas logically and maintaining coherence and in '
        'grammatical accuracy and language range. The ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach that standard. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in connecting ideas logically and maintaining coherence and in '
        'grammatical accuracy and language range. However, performance is still '
        'developing in organising and presenting written work clearly and in adapting '
        'tone and style appropriately to purpose, audience and context and requires '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in connecting ideas logically and maintaining coherence, in grammatical '
        'accuracy and language range, and in adapting tone and style appropriately to '
        'purpose, audience and context. However, the ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. The learner satisfactorily meets the '
        'minimum expected standard for this level in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range. However, '
        'the ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. The learner satisfactorily meets '
        'the minimum expected standard for this level in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range. However, '
        'the ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well established, "
        'while the ability to connect ideas logically and maintain coherence '
        'satisfactorily meets the minimum expected standard for this level. The ability '
        'to organise and present written work clearly is still developing and requires '
        'further consolidation to reach that standard. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well established, "
        'while the ability to connect ideas logically and maintain coherence '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in adapting tone and style appropriately to purpose, audience and '
        'context and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well established. "
        'The learner satisfactorily meets the minimum expected standard for this level '
        'in connecting ideas logically and maintaining coherence and in adapting tone '
        'and style appropriately to purpose, audience and context. However, the ability '
        'to organise and present written work clearly is still developing and requires '
        'further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in grammatical accuracy and "
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident in both assessed areas. The '
        'ability to connect ideas logically and maintain coherence satisfactorily meets '
        'the minimum expected standard for this level. However, the ability to organise '
        'and present written work clearly is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while grammatical accuracy and '
        'language range are also well established. The ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'satisfactorily meets the minimum expected standard for this level. The ability '
        'to organise and present written work clearly is still developing and requires '
        'further consolidation to reach that standard. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in adapting tone and style appropriately to purpose, audience and '
        'context and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The learner satisfactorily meets the minimum expected standard for '
        'this level in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'However, the ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to adapt tone and style appropriately to purpose, '
        'audience and context is also well established. The ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context. The ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'However, the ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. The ability to organise and present written work clearly is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the remaining two assessed areas, '
        'namely grammatical accuracy and language range and adapting tone and style '
        'appropriately to purpose, audience and context, fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. Performance is still developing in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context and requires further consolidation to reach the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range fall well below that standard and require substantial further '
        'development.'
    ),
    ('developing', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while the ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. The ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach that '
        'standard. However, grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context, with confidence evident in both assessed areas. '
        'The ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to connect '
        'ideas logically and maintain coherence is also well established. The ability '
        'to organise and present written work clearly is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. Performance is still developing in organising and presenting '
        'written work clearly and in grammatical accuracy and language range and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'confident', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. However, performance is still developing in organising and '
        'presenting written work clearly, in grammatical accuracy and language range, '
        'and in adapting tone and style appropriately to purpose, audience and context '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('developing', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while the ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. However, performance is still developing in '
        'organising and presenting written work clearly and in grammatical accuracy and '
        'language range and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'developing', 'confident'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context, with confidence evident in both assessed areas. '
        'However, performance is still developing in organising and presenting written '
        'work clearly and in grammatical accuracy and language range and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to connect '
        'ideas logically and maintain coherence is also well established. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in grammatical accuracy and language range and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while grammatical accuracy and language range satisfactorily '
        'meet the minimum expected standard for this level. The ability to organise and '
        'present written work clearly is still developing and requires further '
        'consolidation to reach that standard. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established, while grammatical accuracy and language range satisfactorily '
        'meet the minimum expected standard for this level. However, performance is '
        'still developing in organising and presenting written work clearly and in '
        'adapting tone and style appropriately to purpose, audience and context and '
        'requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'well established. The learner satisfactorily meets the minimum expected '
        'standard for this level in grammatical accuracy and language range and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'However, the ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context, with confidence evident in both assessed areas. '
        'Grammatical accuracy and language range satisfactorily meet the minimum '
        'expected standard for this level. However, the ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach that standard.'
    ),
    ('developing', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to connect '
        'ideas logically and maintain coherence is also well established. Grammatical '
        'accuracy and language range satisfactorily meet the minimum expected standard '
        'for this level. However, the ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('developing', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence and in grammatical accuracy and language range, with '
        'confidence evident in both assessed areas. The ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, the ability to '
        'adapt tone and style appropriately to purpose, audience and context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'confident', 'developing'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence and in grammatical accuracy and language range, with '
        'confidence evident in both assessed areas. However, performance is still '
        'developing in organising and presenting written work clearly and in adapting '
        'tone and style appropriately to purpose, audience and context and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence and in grammatical accuracy and language range, with '
        'confidence evident in both assessed areas. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the '
        'minimum expected standard for this level. However, the ability to organise and '
        'present written work clearly is still developing and requires further '
        'consolidation to reach that standard.'
    ),
    ('developing', 'confident', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in connecting ideas logically "
        'and maintaining coherence, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context, with '
        'confidence evident in all three assessed areas. However, the ability to '
        'organise and present written work clearly is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Performance is well established '
        'in connecting ideas logically and maintaining coherence and in grammatical '
        'accuracy and language range, with confidence evident in both assessed areas. '
        'However, the ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence is '
        'also well established. The ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, the ability to adapt tone '
        'and style appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('developing', 'confident', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence is '
        'also well established. However, performance is still developing in organising '
        'and presenting written work clearly and in adapting tone and style '
        'appropriately to purpose, audience and context and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to connect ideas logically and maintain coherence is '
        'also well established. The ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'confident', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Performance is well established in connecting ideas logically and '
        'maintaining coherence and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident in both assessed areas. However, '
        'the ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('developing', 'confident', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in grammatical accuracy and '
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context. The ability to connect ideas logically and maintain '
        'coherence is well established. However, the ability to organise and present '
        'written work clearly is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise and present written work clearly '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the remaining two assessed areas, '
        'namely grammatical accuracy and language range and adapting tone and style '
        'appropriately to purpose, audience and context, fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is still developing in organising and '
        'presenting written work clearly and in adapting tone and style appropriately '
        'to purpose, audience and context and requires further consolidation to reach '
        'the minimum expected standard for this level. However, grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style appropriately '
        'to purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. The ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach that '
        'standard. However, grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('developing', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style appropriately '
        'to purpose, audience and context is also well established. The ability to '
        'organise and present written work clearly is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that standard '
        'and require substantial further development.'
    ),
    ('developing', 'strong', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context. The ability to organise and present written '
        'work clearly is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level. However, grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('developing', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is still developing in organising and '
        'presenting written work clearly and in grammatical accuracy and language range '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, the ability to adapt tone and style appropriately to '
        'purpose, audience and context falls well below that standard and requires '
        'substantial further development.'
    ),
    ('developing', 'strong', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. However, performance is still developing in organising '
        'and presenting written work clearly, in grammatical accuracy and language '
        'range, and in adapting tone and style appropriately to purpose, audience and '
        'context and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style appropriately '
        'to purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. However, performance is still developing in '
        'organising and presenting written work clearly and in grammatical accuracy and '
        'language range and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'developing', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style appropriately '
        'to purpose, audience and context is also well established. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in grammatical accuracy and language range and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context. However, performance is still developing in '
        'organising and presenting written work clearly and in grammatical accuracy and '
        'language range and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('developing', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. The ability '
        'to organise and present written work clearly is still developing and requires '
        'further consolidation to reach that standard. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well below '
        'that standard and requires substantial further development.'
    ),
    ('developing', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'performance is still developing in organising and presenting written work '
        'clearly and in adapting tone and style appropriately to purpose, audience and '
        'context and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The learner satisfactorily meets the minimum expected '
        'standard for this level in grammatical accuracy and language range and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'However, the ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while the ability to adapt tone and style appropriately '
        'to purpose, audience and context is also well established. Grammatical '
        'accuracy and language range satisfactorily meet the minimum expected standard '
        'for this level. However, the ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('developing', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context. Grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, the '
        'ability to organise and present written work clearly is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range are also '
        'well established. The ability to organise and present written work clearly is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('developing', 'strong', 'confident', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range are also '
        'well established. However, performance is still developing in organising and '
        'presenting written work clearly and in adapting tone and style appropriately '
        'to purpose, audience and context and requires further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong, while grammatical accuracy and language range are also '
        'well established. The ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to organise and present written '
        'work clearly is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('developing', 'strong', 'confident', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is well established in grammatical accuracy '
        'and language range and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident in both assessed areas. However, '
        'the ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('developing', 'strong', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in adapting tone and style appropriately to '
        'purpose, audience and context. Grammatical accuracy and language range are '
        'well established. However, the ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in grammatical accuracy and language range. The '
        'ability to organise and present written work clearly is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('developing', 'strong', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in grammatical accuracy and language range. '
        'However, performance is still developing in organising and presenting written '
        'work clearly and in adapting tone and style appropriately to purpose, audience '
        'and context and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('developing', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in grammatical accuracy and language range. The '
        'ability to adapt tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to organise and present written work clearly is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('developing', 'strong', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence and in grammatical accuracy and language range. The '
        'ability to adapt tone and style appropriately to purpose, audience and context '
        'is well established. However, the ability to organise and present written work '
        'clearly is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('developing', 'strong', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in connecting ideas logically '
        'and maintaining coherence, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'However, the ability to organise and present written work clearly is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the other three assessed areas, namely cohesion and the logical connection '
        'of ideas, grammatical accuracy and language range, and appropriate use of '
        'tone and style for purpose, audience and context, fall well below that '
        'standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that '
        'standard. However, the two assessed areas, namely cohesion and the logical '
        'connection of ideas and grammatical accuracy and language range, fall well '
        'below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in adapting tone '
        'and style appropriately to purpose, audience and context. However, the two '
        'assessed areas, namely cohesion and the logical connection of ideas and '
        'grammatical accuracy and language range, fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, the two assessed areas, namely cohesion '
        'and the logical connection of ideas and grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to organise '
        'and present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, the two assessed areas, namely cohesion '
        'and the logical connection of ideas and grammatical accuracy and language '
        'range, fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. '
        'Grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard. However, the two assessed '
        'areas, namely cohesion and the logical connection of ideas and appropriate '
        'use of tone and style for purpose, audience and context, fall well below '
        'that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. '
        'Grammatical accuracy and language range and appropriate use of tone and '
        'style for purpose, audience and context are still developing and require '
        'further consolidation to reach that standard. However, the ability to '
        'connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in adapting tone '
        'and style appropriately to purpose, audience and context. Grammatical '
        'accuracy and language range are still developing and require further '
        'consolidation to reach that standard. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. Grammatical accuracy and language range are still '
        'developing and require further consolidation to reach that standard. '
        'However, the ability to connect ideas logically and maintain coherence falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to organise '
        'and present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. Grammatical accuracy and language range are still '
        'developing and require further consolidation to reach that standard. '
        'However, the ability to connect ideas logically and maintain coherence falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in using grammar '
        'accurately and drawing on an appropriate range of language. However, the two '
        'assessed areas, namely cohesion and the logical connection of ideas and '
        'appropriate use of tone and style for purpose, audience and context, fall '
        'well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in using grammar '
        'accurately and drawing on an appropriate range of language. The ability to '
        'adapt tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to connect ideas logically and maintain coherence falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly, in using grammar '
        'accurately and drawing on an appropriate range of language, and in adapting '
        'tone and style appropriately to purpose, audience and context. However, the '
        'ability to connect ideas logically and maintain coherence falls well below '
        'that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Organisation and the clear '
        'presentation of written work and grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Organisation and the clear '
        'presentation of written work and grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the two assessed areas, namely cohesion and the logical connection of ideas '
        'and appropriate use of tone and style for purpose, audience and context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that '
        'standard. However, the ability to connect ideas logically and maintain '
        'coherence falls well below that standard and requires substantial further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. Organisation and the clear presentation of written work and '
        'appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s abilities to use grammar accurately and draw on a varied "
        'range of language and to adapt tone and style appropriately to purpose, '
        'audience and context are well established, with confidence evident in both '
        'assessed areas. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Grammatical accuracy and '
        'language range are also well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the two assessed areas, namely cohesion and the logical connection of ideas '
        'and appropriate use of tone and style for purpose, audience and context, '
        'fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that '
        'standard. However, the ability to connect ideas logically and maintain '
        'coherence falls well below that standard and requires substantial further '
        'development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Organisation and the clear presentation of written work and '
        'appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to adapt tone and style appropriately to purpose, '
        'audience and context is also well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'needs_work', 'strong', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in using grammar '
        'accurately and drawing on an appropriate range of language and in adapting '
        'tone and style appropriately to purpose, audience and context, while the '
        'ability to organise and present written work clearly satisfactorily meets '
        'the minimum expected standard for this level. However, the ability to '
        'connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the two assessed areas, namely grammatical accuracy and language '
        'range and appropriate use of tone and style for purpose, audience and '
        'context, fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. Cohesion '
        'and the logical connection of ideas and appropriate use of tone and style '
        'for purpose, audience and context are still developing and require further '
        'consolidation to reach that standard. However, grammatical accuracy and '
        'language range fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in adapting tone '
        'and style appropriately to purpose, audience and context. The ability to '
        'connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach that standard. However, grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. The ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach '
        'that standard. However, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('satisfactory', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to organise '
        'and present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. The ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach '
        'that standard. However, grammatical accuracy and language range fall well '
        'below that standard and require substantial further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. Cohesion '
        'and the logical connection of ideas and grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that '
        'standard. However, the ability to adapt tone and style appropriately to '
        'purpose, audience and context falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'developing', 'developing', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly "
        'satisfactorily meets the minimum expected standard for this level. However, '
        'cohesion and the logical connection of ideas, grammatical accuracy and '
        'language range, and appropriate use of tone and style for purpose, audience '
        'and context are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'developing', 'developing', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in adapting tone '
        'and style appropriately to purpose, audience and context. However, cohesion '
        'and the logical connection of ideas and grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that '
        'standard.'
    ),
    ('satisfactory', 'developing', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, cohesion and the logical connection of '
        'ideas and grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong, while the ability to organise '
        'and present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, cohesion and the logical connection of '
        'ideas and grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in using grammar '
        'accurately and drawing on an appropriate range of language. The ability to '
        'connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach that standard. However, the ability '
        'to adapt tone and style appropriately to purpose, audience and context falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in using grammar '
        'accurately and drawing on an appropriate range of language. However, '
        'cohesion and the logical connection of ideas and appropriate use of tone and '
        'style for purpose, audience and context are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly, in using grammar '
        'accurately and drawing on an appropriate range of language, and in adapting '
        'tone and style appropriately to purpose, audience and context. However, the '
        'ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Organisation and the clear '
        'presentation of written work and grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Organisation and the clear '
        'presentation of written work and grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'developing', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'cohesion and the logical connection of ideas and appropriate use of tone and '
        'style for purpose, audience and context are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. Organisation and the clear presentation of written work and '
        'appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'confident'): (
        "{learner_name}'s abilities to use grammar accurately and draw on a varied "
        'range of language and to adapt tone and style appropriately to purpose, '
        'audience and context are well established, with confidence evident in both '
        'assessed areas. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Grammatical accuracy and '
        'language range are also well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to '
        'reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. The '
        'ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard. '
        'However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'developing', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong, while the ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'cohesion and the logical connection of ideas and appropriate use of tone and '
        'style for purpose, audience and context are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Organisation and the clear presentation of written work and '
        'appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to adapt tone and style appropriately to purpose, '
        'audience and context is also well established. The ability to organise and '
        'present written work clearly satisfactorily meets the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to '
        'reach that standard.'
    ),
    ('satisfactory', 'developing', 'strong', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in using grammar '
        'accurately and drawing on an appropriate range of language and in adapting '
        'tone and style appropriately to purpose, audience and context, while the '
        'ability to organise and present written work clearly satisfactorily meets '
        'the minimum expected standard for this level. However, the ability to '
        'connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in connecting '
        'ideas logically and maintaining coherence. However, the two assessed areas, '
        'namely grammatical accuracy and language range and appropriate use of tone '
        'and style for purpose, audience and context, fall well below that standard '
        'and require substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in connecting '
        'ideas logically and maintaining coherence. The ability to adapt tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach that standard. However, grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly, in connecting ideas '
        'logically and maintaining coherence, and in adapting tone and style '
        'appropriately to purpose, audience and context. However, grammatical '
        'accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Organisation and the clear '
        'presentation of written work and cohesion and the logical connection of '
        'ideas satisfactorily meet the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Organisation and the clear '
        'presentation of written work and cohesion and the logical connection of '
        'ideas satisfactorily meet the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in connecting '
        'ideas logically and maintaining coherence. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that '
        'standard. However, the ability to adapt tone and style appropriately to '
        'purpose, audience and context falls well below that standard and requires '
        'substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly and in connecting '
        'ideas logically and maintaining coherence. However, grammatical accuracy and '
        'language range and appropriate use of tone and style for purpose, audience '
        'and context are still developing and require further consolidation to reach '
        'that standard.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'satisfactory'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly, in connecting ideas '
        'logically and maintaining coherence, and in adapting tone and style '
        'appropriately to purpose, audience and context. However, grammatical '
        'accuracy and language range are still developing and require further '
        'consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Organisation and the clear '
        'presentation of written work and cohesion and the logical connection of '
        'ideas satisfactorily meet the minimum expected standard for this level. '
        'However, grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Organisation and the clear '
        'presentation of written work and cohesion and the logical connection of '
        'ideas satisfactorily meet the minimum expected standard for this level. '
        'However, grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'needs_work'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly, in connecting ideas '
        'logically and maintaining coherence, and in using grammar accurately and '
        'drawing on an appropriate range of language. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'developing'): (
        '{learner_name} satisfactorily meets the minimum expected standard for this '
        'level in organising and presenting written work clearly, in connecting ideas '
        'logically and maintaining coherence, and in using grammar accurately and '
        'drawing on an appropriate range of language. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s writing performance satisfactorily meets the minimum "
        'expected standard across all four assessed areas. Organisation and clarity, '
        'cohesion, grammatical accuracy and language range, and appropriate use of '
        'tone and style are all satisfactory for this level, although there is still '
        'scope for further development and consolidation.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is well established. Although organisation and the '
        'clear presentation of written work, cohesion and the logical connection of '
        'ideas, and grammatical accuracy and language range satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for further '
        'development and consolidation in all three areas.'
    ),
    ('satisfactory', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Although organisation and the '
        'clear presentation of written work, cohesion and the logical connection of '
        'ideas, and grammatical accuracy and language range satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for further '
        'development and consolidation in all three areas.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. Organisation and the clear presentation of written work and '
        'cohesion and the logical connection of ideas satisfactorily meet the minimum '
        'expected standard for this level. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. Organisation and the clear presentation of written work and '
        'cohesion and the logical connection of ideas satisfactorily meet the minimum '
        'expected standard for this level. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are well "
        'established. Although organisation and the clear presentation of written '
        'work, cohesion and the logical connection of ideas, and appropriate use of '
        'tone and style for purpose, audience and context satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for further '
        'development and consolidation in all three areas.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s abilities to use grammar accurately and draw on a varied "
        'range of language and to adapt tone and style appropriately to purpose, '
        'audience and context are well established, with confidence evident in both '
        'assessed areas. Although organisation and the clear presentation of written '
        'work and cohesion and the logical connection of ideas satisfactorily meet '
        'the minimum expected standard for this level, there is still scope for '
        'further development and consolidation in both areas.'
    ),
    ('satisfactory', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. Grammatical accuracy and '
        'language range are also well established. Although organisation and the '
        'clear presentation of written work and cohesion and the logical connection '
        'of ideas satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Organisation and the clear presentation of written work and cohesion '
        'and the logical connection of ideas satisfactorily meet the minimum expected '
        'standard for this level. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Organisation and the clear presentation of written work and cohesion '
        'and the logical connection of ideas satisfactorily meet the minimum expected '
        'standard for this level. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. Although organisation and the clear presentation of written work, '
        'cohesion and the logical connection of ideas, and appropriate use of tone '
        'and style for purpose, audience and context satisfactorily meet the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in all three areas.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to adapt tone and style appropriately to purpose, '
        'audience and context is also well established. Although organisation and the '
        'clear presentation of written work and cohesion and the logical connection '
        'of ideas satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('satisfactory', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in using grammar '
        'accurately and drawing on an appropriate range of language and in adapting '
        'tone and style appropriately to purpose, audience and context. Although '
        'organisation and the clear presentation of written work and cohesion and the '
        'logical connection of ideas satisfactorily meet the minimum expected '
        'standard for this level, there is still scope for further development and '
        'consolidation in both areas.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. The ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level. '
        'However, the two assessed areas, namely grammatical accuracy and language '
        'range and appropriate use of tone and style for purpose, audience and '
        'context, fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. The ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level. '
        'The ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that '
        'standard. However, grammatical accuracy and language range fall well below '
        'that standard and require substantial further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. Organisation and the clear presentation of written work '
        'and appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s abilities to connect ideas logically and maintain coherence "
        'and to adapt tone and style appropriately to purpose, audience and context '
        'are well established, with confidence evident in both assessed areas. The '
        'ability to organise and present written work clearly satisfactorily meets '
        'the minimum expected standard for this level. However, grammatical accuracy '
        'and language range fall well below that standard and require substantial '
        'further development.'
    ),
    ('satisfactory', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. The ability to connect ideas '
        'logically and maintain coherence is also well established. The ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. The ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level. '
        'Grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. The ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level. '
        'However, grammatical accuracy and language range and appropriate use of tone '
        'and style for purpose, audience and context are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. Organisation and the clear presentation of written work '
        'and appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'developing', 'confident'): (
        "{learner_name}'s abilities to connect ideas logically and maintain coherence "
        'and to adapt tone and style appropriately to purpose, audience and context '
        'are well established, with confidence evident in both assessed areas. The '
        'ability to organise and present written work clearly satisfactorily meets '
        'the minimum expected standard for this level. However, grammatical accuracy '
        'and language range are still developing and require further consolidation to '
        'reach that standard.'
    ),
    ('satisfactory', 'confident', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. The ability to connect ideas '
        'logically and maintain coherence is also well established. The ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that '
        'standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. Organisation and the clear presentation of written work '
        'and grammatical accuracy and language range satisfactorily meet the minimum '
        'expected standard for this level. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. Organisation and the clear presentation of written work '
        'and grammatical accuracy and language range satisfactorily meet the minimum '
        'expected standard for this level. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is well established. Although organisation and the clear presentation of '
        'written work, grammatical accuracy and language range, and appropriate use '
        'of tone and style for purpose, audience and context satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for further '
        'development and consolidation in all three areas.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s abilities to connect ideas logically and maintain coherence "
        'and to adapt tone and style appropriately to purpose, audience and context '
        'are well established, with confidence evident in both assessed areas. '
        'Although organisation and the clear presentation of written work and '
        'grammatical accuracy and language range satisfactorily meet the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in both areas.'
    ),
    ('satisfactory', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. The ability to connect ideas '
        'logically and maintain coherence is also well established. Although '
        'organisation and the clear presentation of written work and grammatical '
        'accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, there is still scope for further development and '
        'consolidation in both areas.'
    ),
    ('satisfactory', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s abilities to connect ideas logically and maintain coherence "
        'and to use grammar accurately and draw on a varied range of language are '
        'well established, with confidence evident in both assessed areas. The '
        'ability to organise and present written work clearly satisfactorily meets '
        'the minimum expected standard for this level. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'confident', 'confident', 'developing'): (
        "{learner_name}'s abilities to connect ideas logically and maintain coherence "
        'and to use grammar accurately and draw on a varied range of language are '
        'well established, with confidence evident in both assessed areas. The '
        'ability to organise and present written work clearly satisfactorily meets '
        'the minimum expected standard for this level. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s abilities to connect ideas logically and maintain coherence "
        'and to use grammar accurately and draw on a varied range of language are '
        'well established, with confidence evident in both assessed areas. Although '
        'organisation and the clear presentation of written work and appropriate use '
        'of tone and style for purpose, audience and context satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for further '
        'development and consolidation in both areas.'
    ),
    ('satisfactory', 'confident', 'confident', 'confident'): (
        "{learner_name}'s abilities to connect ideas logically and maintain "
        'coherence, to use grammar accurately and draw on a varied range of language, '
        'and to adapt tone and style appropriately to purpose, audience and context '
        'are well established, with confidence evident in all three assessed areas. '
        'Although the ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('satisfactory', 'confident', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, "
        'audience and context is particularly strong. The abilities to connect ideas '
        'logically and maintain coherence and to use grammar accurately and draw on a '
        'varied range of language are well established, with confidence evident in '
        'both assessed areas. Although the ability to organise and present written '
        'work clearly satisfactorily meets the minimum expected standard for this '
        'level, there is still scope for further development and consolidation in '
        'this area.'
    ),
    ('satisfactory', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to connect ideas logically and maintain coherence is '
        'also well established. The ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level. '
        'However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('satisfactory', 'confident', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to connect ideas logically and maintain coherence is '
        'also well established. The ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level. '
        'However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context is still developing and requires further consolidation '
        'to reach that standard.'
    ),
    ('satisfactory', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The ability to connect ideas logically and maintain coherence is '
        'also well established. Although organisation and the clear presentation of '
        'written work and appropriate use of tone and style for purpose, audience and '
        'context satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('satisfactory', 'confident', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly "
        'strong. The abilities to connect ideas logically and maintain coherence and '
        'to adapt tone and style appropriately to purpose, audience and context are '
        'well established, with confidence evident in both assessed areas. Although '
        'the ability to organise and present written work clearly satisfactorily '
        'meets the minimum expected standard for this level, there is still scope for '
        'further development and consolidation in this area.'
    ),
    ('satisfactory', 'confident', 'strong', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in using grammar '
        'accurately and drawing on an appropriate range of language and in adapting '
        'tone and style appropriately to purpose, audience and context. The ability '
        'to connect ideas logically and maintain coherence is also well established. '
        'Although the ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong, while the ability to organise and present written '
        'work clearly satisfactorily meets the minimum expected standard for this '
        'level. However, the two assessed areas, namely grammatical accuracy and '
        'language range and appropriate use of tone and style for purpose, audience '
        'and context, fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong, while the ability to organise and present written '
        'work clearly satisfactorily meets the minimum expected standard for this '
        'level. The ability to adapt tone and style appropriately to purpose, '
        'audience and context is still developing and requires further consolidation '
        'to reach that standard. However, grammatical accuracy and language range '
        'fall well below that standard and require substantial further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Organisation and the clear presentation of written '
        'work and appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. The ability to adapt tone and style appropriately to '
        'purpose, audience and context is also well established. The ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'strong', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context, while the ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range fall well below that standard and require substantial further '
        'development.'
    ),
    ('satisfactory', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong, while the ability to organise and present written '
        'work clearly satisfactorily meets the minimum expected standard for this '
        'level. Grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard. However, the ability '
        'to adapt tone and style appropriately to purpose, audience and context falls '
        'well below that standard and requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong, while the ability to organise and present written '
        'work clearly satisfactorily meets the minimum expected standard for this '
        'level. However, grammatical accuracy and language range and appropriate use '
        'of tone and style for purpose, audience and context are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Organisation and the clear presentation of written '
        'work and appropriate use of tone and style for purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level. However, '
        'grammatical accuracy and language range are still developing and require '
        'further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'developing', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. The ability to adapt tone and style appropriately to '
        'purpose, audience and context is also well established. The ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that '
        'standard.'
    ),
    ('satisfactory', 'strong', 'developing', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context, while the ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that '
        'standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Organisation and the clear presentation of written '
        'work and grammatical accuracy and language range satisfactorily meet the '
        'minimum expected standard for this level. However, the ability to adapt tone '
        'and style appropriately to purpose, audience and context falls well below '
        'that standard and requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Organisation and the clear presentation of written '
        'work and grammatical accuracy and language range satisfactorily meet the '
        'minimum expected standard for this level. However, the ability to adapt tone '
        'and style appropriately to purpose, audience and context is still developing '
        'and requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Although organisation and the clear presentation of '
        'written work, grammatical accuracy and language range, and appropriate use '
        'of tone and style for purpose, audience and context satisfactorily meet the '
        'minimum expected standard for this level, there is still scope for further '
        'development and consolidation in all three areas.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. The ability to adapt tone and style appropriately to '
        'purpose, audience and context is also well established. Although '
        'organisation and the clear presentation of written work and grammatical '
        'accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level, there is still scope for further development and '
        'consolidation in both areas.'
    ),
    ('satisfactory', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context. Although organisation and '
        'the clear presentation of written work and grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('satisfactory', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Grammatical accuracy and language range are also '
        'well established. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to adapt tone and style appropriately to purpose, audience and '
        'context falls well below that standard and requires substantial further '
        'development.'
    ),
    ('satisfactory', 'strong', 'confident', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Grammatical accuracy and language range are also '
        'well established. The ability to organise and present written work clearly '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('satisfactory', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. Grammatical accuracy and language range are also '
        'well established. Although organisation and the clear presentation of '
        'written work and appropriate use of tone and style for purpose, audience and '
        'context satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('satisfactory', 'strong', 'confident', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence "
        'is particularly strong. The abilities to use grammar accurately and draw on '
        'a varied range of language and to adapt tone and style appropriately to '
        'purpose, audience and context are well established, with confidence evident '
        'in both assessed areas. Although the ability to organise and present written '
        'work clearly satisfactorily meets the minimum expected standard for this '
        'level, there is still scope for further development and consolidation in '
        'this area.'
    ),
    ('satisfactory', 'strong', 'confident', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context. Grammatical accuracy and '
        'language range are also well established. Although the ability to organise '
        'and present written work clearly satisfactorily meets the minimum expected '
        'standard for this level, there is still scope for further development and '
        'consolidation in this area.'
    ),
    ('satisfactory', 'strong', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in using grammar accurately '
        'and drawing on an appropriate range of language, while the ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('satisfactory', 'strong', 'strong', 'developing'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in using grammar accurately '
        'and drawing on an appropriate range of language, while the ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('satisfactory', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in using grammar accurately '
        'and drawing on an appropriate range of language. Although organisation and '
        'the clear presentation of written work and appropriate use of tone and style '
        'for purpose, audience and context satisfactorily meet the minimum expected '
        'standard for this level, there is still scope for further development and '
        'consolidation in both areas.'
    ),
    ('satisfactory', 'strong', 'strong', 'confident'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence and in using grammar accurately '
        'and drawing on an appropriate range of language. The ability to adapt tone '
        'and style appropriately to purpose, audience and context is also well '
        'established. Although the ability to organise and present written work '
        'clearly satisfactorily meets the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in this area.'
    ),
    ('satisfactory', 'strong', 'strong', 'strong'): (
        '{learner_name} demonstrates particularly strong abilities in connecting '
        'ideas logically and maintaining coherence, in using grammar accurately and '
        'drawing on an appropriate range of language, and in adapting tone and style '
        'appropriately to purpose, audience and context. Although the ability to '
        'organise and present written work clearly satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further '
        'development and consolidation in this area.'
    ),
    ('confident', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. However, the ability to connect '
        'ideas logically and maintain coherence, grammatical accuracy and language range, and '
        'the ability to adapt tone and style appropriately to purpose, audience and context '
        'fall well below the minimum expected standard for this level and require substantial '
        'further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence and grammatical accuracy '
        'and language range fall well below that standard and require substantial further '
        'development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence and grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. However, the ability '
        'to connect ideas logically and maintain coherence and grammatical accuracy and '
        'language range fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'needs_work', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. However, '
        'the ability to connect ideas logically and maintain coherence and grammatical accuracy '
        'and language range fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range are still developing and require further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence and the ability to adapt tone and style appropriately to purpose, '
        'audience and context fall well below that standard and require substantial further '
        'development.'
    ),
    ('confident', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range and the ability to adapt tone and style appropriately to purpose, audience and '
        'context are still developing and require further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence falls well below that standard and requires substantial further '
        'development.'
    ),
    ('confident', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. Grammatical accuracy and language range are still '
        'developing and require further consolidation to reach that standard. However, the '
        'ability to connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. Grammatical accuracy '
        'and language range are still developing and require further consolidation to reach the '
        'minimum expected standard for this level. However, the ability to connect ideas '
        'logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('confident', 'needs_work', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. '
        'Grammatical accuracy and language range are still developing and require further '
        'consolidation to reach the minimum expected standard for this level. However, the '
        'ability to connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level. However, the '
        'ability to connect ideas logically and maintain coherence and the ability to adapt '
        'tone and style appropriately to purpose, audience and context fall well below that '
        'standard and require substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level. The ability to '
        'adapt tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard. However, the '
        'ability to connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range and the ability to adapt tone and style appropriately to purpose, audience and '
        'context satisfactorily meet the minimum expected standard for this level. However, the '
        'ability to connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. Grammatical accuracy '
        'and language range satisfactorily meet the minimum expected standard for this level. '
        'However, the ability to connect ideas logically and maintain coherence falls well '
        'below that standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. '
        'Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and maintain '
        'coherence falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. However, the ability to connect ideas logically and '
        'maintain coherence and the ability to adapt tone and style appropriately to purpose, '
        'audience and context fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. The ability to adapt tone and style appropriately to '
        'purpose, audience and context is still developing and requires further consolidation '
        'to reach the minimum expected standard for this level. However, the ability to connect '
        'ideas logically and maintain coherence falls well below that standard and requires '
        'substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. The ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, the ability to connect ideas logically and maintain coherence '
        'falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, grammatical accuracy and language range, and adapting tone '
        'and style appropriately to purpose, audience and context, with confidence evident '
        'across these areas. However, the ability to connect ideas logically and maintain '
        'coherence falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('confident', 'needs_work', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly and grammatical accuracy and language range, '
        'with confidence evident across both areas. However, the ability to connect ideas '
        'logically and maintain coherence falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. However, the ability to connect ideas logically '
        'and maintain coherence and the ability to adapt tone and style appropriately to '
        'purpose, audience and context fall well below the minimum expected standard for this '
        'level and require substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level. However, '
        'the ability to connect ideas logically and maintain coherence falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence falls well below that standard and requires substantial further '
        'development.'
    ),
    ('confident', 'needs_work', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and adapting tone and style appropriately to purpose, audience and context, '
        'with confidence evident across both areas. However, the ability to connect ideas '
        'logically and maintain coherence falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('confident', 'needs_work', 'strong', 'strong'): (
        "{learner_name}'s writing is particularly strong in grammatical accuracy and language "
        'range and adapting tone and style appropriately to purpose, audience and context. The '
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. However, the ability to connect ideas logically '
        'and maintain coherence falls well below the minimum expected standard for this level '
        'and requires substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'grammatical accuracy and language range and the ability to adapt tone and style '
        'appropriately to purpose, audience and context fall well below that standard and '
        'require substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence and the ability to adapt tone and style appropriately '
        'to purpose, audience and context are still developing and require further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'grammatical accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. The ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach that '
        'standard. However, grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. The ability to '
        'connect ideas logically and maintain coherence is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level. However, '
        'grammatical accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('confident', 'developing', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. The '
        'ability to connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('confident', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence and grammatical accuracy and language range are still '
        'developing and require further consolidation to reach the minimum expected standard '
        'for this level. However, the ability to adapt tone and style appropriately to purpose, '
        'audience and context falls well below that standard and requires substantial further '
        'development.'
    ),
    ('confident', 'developing', 'developing', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. However, the ability to connect '
        'ideas logically and maintain coherence, grammatical accuracy and language range, and '
        'the ability to adapt tone and style appropriately to purpose, audience and context are '
        'still developing and require further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('confident', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence and grammatical accuracy and language range are still developing '
        'and require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'developing', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. However, the ability '
        'to connect ideas logically and maintain coherence and grammatical accuracy and '
        'language range are still developing and require further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. However, '
        'the ability to connect ideas logically and maintain coherence and grammatical accuracy '
        'and language range are still developing and require further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level. The ability to '
        'connect ideas logically and maintain coherence is still developing and requires '
        'further consolidation to reach that standard. However, the ability to adapt tone and '
        'style appropriately to purpose, audience and context falls well below that standard '
        'and requires substantial further development.'
    ),
    ('confident', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level. However, the '
        'ability to connect ideas logically and maintain coherence and the ability to adapt '
        'tone and style appropriately to purpose, audience and context are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Grammatical accuracy and language '
        'range and the ability to adapt tone and style appropriately to purpose, audience and '
        'context satisfactorily meet the minimum expected standard for this level. However, the '
        'ability to connect ideas logically and maintain coherence is still developing and '
        'requires further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. Grammatical accuracy '
        'and language range satisfactorily meet the minimum expected standard for this level. '
        'However, the ability to connect ideas logically and maintain coherence is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. '
        'Grammatical accuracy and language range satisfactorily meet the minimum expected '
        'standard for this level. However, the ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach that '
        'standard.'
    ),
    ('confident', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. The ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard and '
        'requires substantial further development.'
    ),
    ('confident', 'developing', 'confident', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. However, the ability to connect ideas logically and '
        'maintain coherence and the ability to adapt tone and style appropriately to purpose, '
        'audience and context are still developing and require further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. The ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, the ability to connect ideas logically and maintain coherence is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'developing', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, grammatical accuracy and language range, and adapting tone '
        'and style appropriately to purpose, audience and context, with confidence evident '
        'across these areas. However, the ability to connect ideas logically and maintain '
        'coherence is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'developing', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly and grammatical accuracy and language range, '
        'with confidence evident across both areas. However, the ability to connect ideas '
        'logically and maintain coherence is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. The ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard and '
        'requires substantial further development.'
    ),
    ('confident', 'developing', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. However, the ability to connect ideas logically '
        'and maintain coherence and the ability to adapt tone and style appropriately to '
        'purpose, audience and context are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. However, the ability to connect ideas logically and '
        'maintain coherence is still developing and requires further consolidation to reach '
        'that standard.'
    ),
    ('confident', 'developing', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and adapting tone and style appropriately to purpose, audience and context, '
        'with confidence evident across both areas. However, the ability to connect ideas '
        'logically and maintain coherence is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'developing', 'strong', 'strong'): (
        "{learner_name}'s writing is particularly strong in grammatical accuracy and language "
        'range and adapting tone and style appropriately to purpose, audience and context. The '
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. However, the ability to connect ideas logically '
        'and maintain coherence is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected standard '
        'for this level. However, grammatical accuracy and language range and the ability to '
        'adapt tone and style appropriately to purpose, audience and context fall well below '
        'that standard and require substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected standard '
        'for this level. The ability to adapt tone and style appropriately to purpose, audience '
        'and context is still developing and requires further consolidation to reach that '
        'standard. However, grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence and the ability to adapt tone and style appropriately '
        'to purpose, audience and context satisfactorily meet the minimum expected standard for '
        'this level. However, grammatical accuracy and language range fall well below that '
        'standard and require substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. The ability to '
        'connect ideas logically and maintain coherence satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language range '
        'fall well below that standard and require substantial further development.'
    ),
    ('confident', 'satisfactory', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. The '
        'ability to connect ideas logically and maintain coherence satisfactorily meets the '
        'minimum expected standard for this level. However, grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected standard '
        'for this level. Grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard. However, the ability to adapt '
        'tone and style appropriately to purpose, audience and context falls well below that '
        'standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected standard '
        'for this level. However, grammatical accuracy and language range and the ability to '
        'adapt tone and style appropriately to purpose, audience and context are still '
        'developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence and the ability to adapt tone and style appropriately '
        'to purpose, audience and context satisfactorily meet the minimum expected standard for '
        'this level. However, grammatical accuracy and language range are still developing and '
        'require further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. The ability to '
        'connect ideas logically and maintain coherence satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language range are '
        'still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. The '
        'ability to connect ideas logically and maintain coherence satisfactorily meets the '
        'minimum expected standard for this level. However, grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence and grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, the ability '
        'to adapt tone and style appropriately to purpose, audience and context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. The ability to connect ideas '
        'logically and maintain coherence and grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, the ability '
        'to adapt tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise written work and present ideas clearly is well "
        'established, with confidence evident in this area. Although the ability to connect '
        'ideas logically and maintain coherence, grammatical accuracy and language range, and '
        'the ability to adapt tone and style appropriately to purpose, audience and context '
        'satisfactorily meet the minimum expected standard for this level, there is still scope '
        'for further development and consolidation in these areas.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. Although the ability '
        'to connect ideas logically and maintain coherence and grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this level, there '
        'is still scope for further development and consolidation in both areas.'
    ),
    ('confident', 'satisfactory', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. The ability to organise written work and present '
        'ideas clearly is also well established, with confidence evident in this area. Although '
        'the ability to connect ideas logically and maintain coherence and grammatical accuracy '
        'and language range satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both areas.'
    ),
    ('confident', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. The ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to adapt tone and style appropriately to purpose, audience and context '
        'falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. The ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level. However, '
        'the ability to adapt tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas. Although the ability to connect ideas logically and '
        'maintain coherence and the ability to adapt tone and style appropriately to purpose, '
        'audience and context satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in both areas.'
    ),
    ('confident', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, grammatical accuracy and language range, and adapting tone '
        'and style appropriately to purpose, audience and context, with confidence evident '
        'across these areas. Although the ability to connect ideas logically and maintain '
        'coherence satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('confident', 'satisfactory', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly and grammatical accuracy and language range, '
        'with confidence evident across both areas. Although the ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected standard '
        'for this level, there is still scope for further development and consolidation in this '
        'area.'
    ),
    ('confident', 'satisfactory', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. The ability to connect ideas logically and '
        'maintain coherence satisfactorily meets the minimum expected standard for this level. '
        'However, the ability to adapt tone and style appropriately to purpose, audience and '
        'context falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'satisfactory', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. The ability to connect ideas logically and '
        'maintain coherence satisfactorily meets the minimum expected standard for this level. '
        'However, the ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'satisfactory', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. The "
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. Although the ability to connect ideas logically '
        'and maintain coherence and the ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meet the minimum expected standard for '
        'this level, there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('confident', 'satisfactory', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and adapting tone and style appropriately to purpose, audience and context, '
        'with confidence evident across both areas. Although the ability to connect ideas '
        'logically and maintain coherence satisfactorily meets the minimum expected standard '
        'for this level, there is still scope for further development and consolidation in this '
        'area.'
    ),
    ('confident', 'satisfactory', 'strong', 'strong'): (
        "{learner_name}'s writing is particularly strong in grammatical accuracy and language "
        'range and adapting tone and style appropriately to purpose, audience and context. The '
        'ability to organise written work and present ideas clearly is also well established, '
        'with confidence evident in this area. Although the ability to connect ideas logically '
        'and maintain coherence satisfactorily meets the minimum expected standard for this '
        'level, there is still scope for further development and consolidation in this area.'
    ),
    ('confident', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. However, grammatical accuracy and language '
        'range and the ability to adapt tone and style appropriately to purpose, audience and '
        'context fall well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. The ability to adapt tone and style '
        'appropriately to purpose, audience and context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level. However, '
        'grammatical accuracy and language range fall well below that standard and require '
        'substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language range '
        'fall well below that standard and require substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, connecting ideas logically and maintaining coherence, and '
        'adapting tone and style appropriately to purpose, audience and context, with '
        'confidence evident across these areas. However, grammatical accuracy and language '
        'range fall well below the minimum expected standard for this level and require '
        'substantial further development.'
    ),
    ('confident', 'confident', 'needs_work', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly and connecting ideas logically and '
        'maintaining coherence, with confidence evident across both areas. However, grammatical '
        'accuracy and language range fall well below the minimum expected standard for this '
        'level and require substantial further development.'
    ),
    ('confident', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. Grammatical accuracy and language range are '
        'still developing and require further consolidation to reach the minimum expected '
        'standard for this level. However, the ability to adapt tone and style appropriately to '
        'purpose, audience and context falls well below that standard and requires substantial '
        'further development.'
    ),
    ('confident', 'confident', 'developing', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. However, grammatical accuracy and language '
        'range and the ability to adapt tone and style appropriately to purpose, audience and '
        'context are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. The ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level. However, grammatical accuracy and language range are '
        'still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'confident', 'developing', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, connecting ideas logically and maintaining coherence, and '
        'adapting tone and style appropriately to purpose, audience and context, with '
        'confidence evident across these areas. However, grammatical accuracy and language '
        'range are still developing and require further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'confident', 'developing', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly and connecting ideas logically and '
        'maintaining coherence, with confidence evident across both areas. However, grammatical '
        'accuracy and language range are still developing and require further consolidation to '
        'reach the minimum expected standard for this level.'
    ),
    ('confident', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. Grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, the ability '
        'to adapt tone and style appropriately to purpose, audience and context falls well '
        'below that standard and requires substantial further development.'
    ),
    ('confident', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. Grammatical accuracy and language range '
        'satisfactorily meet the minimum expected standard for this level. However, the ability '
        'to adapt tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly and connecting ideas logically and maintaining coherence, '
        'with confidence evident across both areas. Although grammatical accuracy and language '
        'range and the ability to adapt tone and style appropriately to purpose, audience and '
        'context satisfactorily meet the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in both areas.'
    ),
    ('confident', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, connecting ideas logically and maintaining coherence, and '
        'adapting tone and style appropriately to purpose, audience and context, with '
        'confidence evident across these areas. Although grammatical accuracy and language '
        'range satisfactorily meet the minimum expected standard for this level, there is still '
        'scope for further development and consolidation in this area.'
    ),
    ('confident', 'confident', 'satisfactory', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly and connecting ideas logically and '
        'maintaining coherence, with confidence evident across both areas. Although grammatical '
        'accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, there is still scope for further development and consolidation in this area.'
    ),
    ('confident', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, connecting ideas logically and maintaining coherence, and '
        'grammatical accuracy and language range, with confidence evident across these areas. '
        'However, the ability to adapt tone and style appropriately to purpose, audience and '
        'context falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('confident', 'confident', 'confident', 'developing'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, connecting ideas logically and maintaining coherence, and '
        'grammatical accuracy and language range, with confidence evident across these areas. '
        'However, the ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('confident', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s performance is well established in organising written work and "
        'presenting ideas clearly, connecting ideas logically and maintaining coherence, and '
        'grammatical accuracy and language range, with confidence evident across these areas. '
        'Although the ability to adapt tone and style appropriately to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('confident', 'confident', 'confident', 'confident'): (
        "{learner_name}'s writing performance is well established across all four assessed "
        'areas. Organisation and clear presentation, cohesion, grammatical accuracy and '
        'language range, and register are all handled with confidence at this level.'
    ),
    ('confident', 'confident', 'confident', 'strong'): (
        "{learner_name}'s ability to adapt tone and style appropriately to purpose, audience "
        'and context is particularly strong. Performance is also well established in organising '
        'written work and presenting ideas clearly, connecting ideas logically and maintaining '
        'coherence, and grammatical accuracy and language range, with confidence evident across '
        'these areas.'
    ),
    ('confident', 'confident', 'strong', 'needs_work'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and connecting ideas logically and maintaining coherence, with confidence '
        'evident across both areas. However, the ability to adapt tone and style appropriately '
        'to purpose, audience and context falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('confident', 'confident', 'strong', 'developing'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and connecting ideas logically and maintaining coherence, with confidence '
        'evident across both areas. However, the ability to adapt tone and style appropriately '
        'to purpose, audience and context is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'confident', 'strong', 'satisfactory'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and connecting ideas logically and maintaining coherence, with confidence '
        'evident across both areas. Although the ability to adapt tone and style appropriately '
        'to purpose, audience and context satisfactorily meets the minimum expected standard '
        'for this level, there is still scope for further development and consolidation in this '
        'area.'
    ),
    ('confident', 'confident', 'strong', 'confident'): (
        "{learner_name}'s grammatical accuracy and language range are particularly strong. "
        'Performance is also well established in organising written work and presenting ideas '
        'clearly, connecting ideas logically and maintaining coherence, and adapting tone and '
        'style appropriately to purpose, audience and context, with confidence evident across '
        'these areas.'
    ),
    ('confident', 'confident', 'strong', 'strong'): (
        "{learner_name}'s writing is particularly strong in grammatical accuracy and language "
        'range and adapting tone and style appropriately to purpose, audience and context. '
        'Performance is also well established in organising written work and presenting ideas '
        'clearly and connecting ideas logically and maintaining coherence, with confidence '
        'evident across both areas.'
    ),
    ('confident', 'strong', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. However, grammatical '
        'accuracy and language range and the ability to adapt tone and style appropriately to '
        'purpose, audience and context fall well below the minimum expected standard for this '
        'level and require substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. The ability to adapt tone '
        'and style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach the minimum expected standard for this level. '
        'However, grammatical accuracy and language range fall well below that standard and '
        'require substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. The ability to adapt tone '
        'and style appropriately to purpose, audience and context satisfactorily meets the '
        'minimum expected standard for this level. However, grammatical accuracy and language '
        'range fall well below that standard and require substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. However, grammatical '
        'accuracy and language range fall well below the minimum expected standard for this '
        'level and require substantial further development.'
    ),
    ('confident', 'strong', 'needs_work', 'strong'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and adapting tone and style appropriately to purpose, audience '
        'and context. The ability to organise written work and present ideas clearly is also '
        'well established, with confidence evident in this area. However, grammatical accuracy '
        'and language range fall well below the minimum expected standard for this level and '
        'require substantial further development.'
    ),
    ('confident', 'strong', 'developing', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. Grammatical accuracy and '
        'language range are still developing and require further consolidation to reach the '
        'minimum expected standard for this level. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below that standard and '
        'requires substantial further development.'
    ),
    ('confident', 'strong', 'developing', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. However, grammatical '
        'accuracy and language range and the ability to adapt tone and style appropriately to '
        'purpose, audience and context are still developing and require further consolidation '
        'to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. The ability to adapt tone '
        'and style appropriately to purpose, audience and context satisfactorily meets the '
        'minimum expected standard for this level. However, grammatical accuracy and language '
        'range are still developing and require further consolidation to reach that standard.'
    ),
    ('confident', 'strong', 'developing', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. However, grammatical '
        'accuracy and language range are still developing and require further consolidation to '
        'reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'developing', 'strong'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and adapting tone and style appropriately to purpose, audience '
        'and context. The ability to organise written work and present ideas clearly is also '
        'well established, with confidence evident in this area. However, grammatical accuracy '
        'and language range are still developing and require further consolidation to reach the '
        'minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. Grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this level. '
        'However, the ability to adapt tone and style appropriately to purpose, audience and '
        'context falls well below that standard and requires substantial further development.'
    ),
    ('confident', 'strong', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. Grammatical accuracy and '
        'language range satisfactorily meet the minimum expected standard for this level. '
        'However, the ability to adapt tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach that standard.'
    ),
    ('confident', 'strong', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. The ability to organise written work and present ideas clearly is '
        'also well established, with confidence evident in this area. Although grammatical '
        'accuracy and language range and the ability to adapt tone and style appropriately to '
        'purpose, audience and context satisfactorily meet the minimum expected standard for '
        'this level, there is still scope for further development and consolidation in both '
        'areas.'
    ),
    ('confident', 'strong', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly and adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across both areas. Although grammatical '
        'accuracy and language range satisfactorily meet the minimum expected standard for this '
        'level, there is still scope for further development and consolidation in this area.'
    ),
    ('confident', 'strong', 'satisfactory', 'strong'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and adapting tone and style appropriately to purpose, audience '
        'and context. The ability to organise written work and present ideas clearly is also '
        'well established, with confidence evident in this area. Although grammatical accuracy '
        'and language range satisfactorily meet the minimum expected standard for this level, '
        'there is still scope for further development and consolidation in this area.'
    ),
    ('confident', 'strong', 'confident', 'needs_work'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly and grammatical accuracy and language range, with '
        'confidence evident across both areas. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'confident', 'developing'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly and grammatical accuracy and language range, with '
        'confidence evident across both areas. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly and grammatical accuracy and language range, with '
        'confidence evident across both areas. Although the ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further development and '
        'consolidation in this area.'
    ),
    ('confident', 'strong', 'confident', 'confident'): (
        "{learner_name}'s ability to connect ideas logically and maintain coherence is "
        'particularly strong. Performance is also well established in organising written work '
        'and presenting ideas clearly, grammatical accuracy and language range, and adapting '
        'tone and style appropriately to purpose, audience and context, with confidence evident '
        'across these areas.'
    ),
    ('confident', 'strong', 'confident', 'strong'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and adapting tone and style appropriately to purpose, audience '
        'and context. Performance is also well established in organising written work and '
        'presenting ideas clearly and grammatical accuracy and language range, with confidence '
        'evident across both areas.'
    ),
    ('confident', 'strong', 'strong', 'needs_work'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and grammatical accuracy and language range. The ability to '
        'organise written work and present ideas clearly is also well established, with '
        'confidence evident in this area. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('confident', 'strong', 'strong', 'developing'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and grammatical accuracy and language range. The ability to '
        'organise written work and present ideas clearly is also well established, with '
        'confidence evident in this area. However, the ability to adapt tone and style '
        'appropriately to purpose, audience and context is still developing and requires '
        'further consolidation to reach the minimum expected standard for this level.'
    ),
    ('confident', 'strong', 'strong', 'satisfactory'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and grammatical accuracy and language range. The ability to '
        'organise written work and present ideas clearly is also well established, with '
        'confidence evident in this area. Although the ability to adapt tone and style '
        'appropriately to purpose, audience and context satisfactorily meets the minimum '
        'expected standard for this level, there is still scope for further development and '
        'consolidation in this area.'
    ),
    ('confident', 'strong', 'strong', 'confident'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence and grammatical accuracy and language range. Performance is also '
        'well established in organising written work and presenting ideas clearly and adapting '
        'tone and style appropriately to purpose, audience and context, with confidence evident '
        'across both areas.'
    ),
    ('confident', 'strong', 'strong', 'strong'): (
        "{learner_name}'s writing is particularly strong in connecting ideas logically and "
        'maintaining coherence, grammatical accuracy and language range, and adapting tone and '
        'style appropriately to purpose, audience and context. The ability to organise written '
        'work and present ideas clearly is also well established, with confidence evident in '
        'this area.'
    ),

    ('strong', 'needs_work', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. However, performance in connecting ideas logically and '
        'maintaining coherence, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is still developing and requires further '
        'consolidation to reach the minimum expected standard for this level. However, '
        'performance in connecting ideas logically and maintaining coherence and in '
        'grammatical accuracy and language range falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. However, performance in connecting ideas logically '
        'and maintaining coherence and in grammatical accuracy and language range falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. However, performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. However, performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, performance in connecting ideas '
        'logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'and in adapting tone and style appropriately to purpose, audience and context '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, performance in connecting ideas '
        'logically and maintaining coherence falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. Performance in grammatical accuracy and language '
        'range is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, performance in connecting '
        'ideas logically and maintaining coherence falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in grammatical accuracy and language range '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, performance in connecting ideas '
        'logically and maintaining coherence falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in grammatical accuracy and language range '
        'is still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, performance in connecting ideas '
        'logically and maintaining coherence falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, performance in connecting ideas '
        'logically and maintaining coherence falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'and in adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in connecting ideas logically and maintaining coherence falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in connecting ideas logically and maintaining coherence falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'needs_work', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in connecting ideas logically and maintaining coherence falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'needs_work', 'confident', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. However, '
        'performance in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'confident', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level. However, performance in connecting ideas '
        'logically and maintaining coherence falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in connecting ideas logically and maintaining coherence falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'needs_work', 'confident', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in grammatical '
        'accuracy and language range and in adapting tone and style appropriately to '
        'purpose, audience and context, with confidence evident across these areas. '
        'However, performance in connecting ideas logically and maintaining coherence '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in grammatical accuracy and language range '
        'is also well established, with confidence evident in this area. However, '
        'performance in connecting ideas logically and maintaining coherence falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'needs_work', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. However, '
        'performance in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, performance in connecting '
        'ideas logically and maintaining coherence falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level. '
        'However, performance in connecting ideas logically and maintaining coherence '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context is also well established, with confidence evident in this area. '
        'However, performance in connecting ideas logically and maintaining coherence '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'needs_work', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'However, performance in connecting ideas logically and maintaining coherence '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, performance in grammatical '
        'accuracy and language range and in adapting tone and style appropriately to '
        'purpose, audience and context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence and in adapting tone and style appropriately to purpose, audience '
        'and context is still developing and requires further consolidation to reach '
        'the minimum expected standard for this level. However, performance in '
        'grammatical accuracy and language range falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. Performance in connecting ideas logically and '
        'maintaining coherence is still developing and requires further consolidation '
        'to reach the minimum expected standard for this level. However, performance in '
        'grammatical accuracy and language range falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in connecting ideas logically and '
        'maintaining coherence is still developing and requires further consolidation '
        'to reach the minimum expected standard for this level. However, performance in '
        'grammatical accuracy and language range falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence is still developing and requires further consolidation '
        'to reach the minimum expected standard for this level. However, performance in '
        'grammatical accuracy and language range falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence and in grammatical accuracy and language range is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, performance in adapting tone and style appropriately to '
        'purpose, audience and context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'developing', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence, in grammatical accuracy and language range, and in adapting tone '
        'and style appropriately to purpose, audience and context is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'developing', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context satisfactorily meets the minimum expected '
        'standard for this level. Performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'developing', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in connecting ideas logically and maintaining coherence is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level. However, performance in adapting tone and style appropriately to '
        'purpose, audience and context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in connecting ideas logically and maintaining coherence and in adapting tone '
        'and style appropriately to purpose, audience and context is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'developing', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range '
        'and in adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in connecting ideas logically and maintaining coherence is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'developing', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in connecting ideas logically and maintaining coherence is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'developing', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in connecting ideas logically and maintaining coherence is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'developing', 'confident', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'connecting ideas logically and maintaining coherence is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, performance in adapting tone and style appropriately to '
        'purpose, audience and context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'confident', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'connecting ideas logically and maintaining coherence and in adapting tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'developing', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in connecting ideas logically and maintaining coherence is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'developing', 'confident', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in grammatical '
        'accuracy and language range and in adapting tone and style appropriately to '
        'purpose, audience and context, with confidence evident across these areas. '
        'Performance in connecting ideas logically and maintaining coherence is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in grammatical accuracy and language range '
        'is also well established, with confidence evident in this area. Performance in '
        'connecting ideas logically and maintaining coherence is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'developing', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level. However, performance in adapting tone and style '
        'appropriately to purpose, audience and context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'developing', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'developing', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level. '
        'Performance in connecting ideas logically and maintaining coherence is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context is also well established, with confidence evident in this area. '
        'Performance in connecting ideas logically and maintaining coherence is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'developing', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'Performance in connecting ideas logically and maintaining coherence is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'However, performance in grammatical accuracy and language range and in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, performance in grammatical '
        'accuracy and language range falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence and in adapting tone and style appropriately to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this level. '
        'However, performance in grammatical accuracy and language range falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in connecting ideas logically and '
        'maintaining coherence satisfactorily meets the minimum expected standard for '
        'this level. However, performance in grammatical accuracy and language range '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'satisfactory', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence satisfactorily meets the minimum expected standard for '
        'this level. However, performance in grammatical accuracy and language range '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'satisfactory', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'Performance in grammatical accuracy and language range is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, performance in adapting tone and style appropriately to '
        'purpose, audience and context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'developing', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence satisfactorily meets the minimum expected standard for this level. '
        'Performance in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'satisfactory', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence and in adapting tone and style appropriately to purpose, audience '
        'and context satisfactorily meets the minimum expected standard for this level. '
        'Performance in grammatical accuracy and language range is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'satisfactory', 'developing', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Performance in connecting ideas logically and '
        'maintaining coherence satisfactorily meets the minimum expected standard for '
        'this level. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'satisfactory', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence satisfactorily meets the minimum expected standard for '
        'this level. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence and in grammatical accuracy and language range satisfactorily meets '
        'the minimum expected standard for this level. However, performance in adapting '
        'tone and style appropriately to purpose, audience and context falls well below '
        'the minimum expected standard for this level and requires substantial further '
        'development.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence and in grammatical accuracy and language range satisfactorily meets '
        'the minimum expected standard for this level. Performance in adapting tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Although performance in connecting ideas logically and '
        'maintaining coherence, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in adapting tone and style appropriately to '
        'purpose, audience and context is also well established, with confidence '
        'evident in this area. Although performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'satisfactory', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Although performance in connecting ideas logically and '
        'maintaining coherence and in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'satisfactory', 'confident', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'connecting ideas logically and maintaining coherence satisfactorily meets the '
        'minimum expected standard for this level. However, performance in adapting '
        'tone and style appropriately to purpose, audience and context falls well below '
        'the minimum expected standard for this level and requires substantial further '
        'development.'
    ),
    ('strong', 'satisfactory', 'confident', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Performance in '
        'connecting ideas logically and maintaining coherence satisfactorily meets the '
        'minimum expected standard for this level. Performance in adapting tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'satisfactory', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in grammatical accuracy and language range is '
        'also well established, with confidence evident in this area. Although '
        'performance in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'satisfactory', 'confident', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in grammatical '
        'accuracy and language range and in adapting tone and style appropriately to '
        'purpose, audience and context, with confidence evident across these areas. '
        'Although performance in connecting ideas logically and maintaining coherence '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'satisfactory', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in grammatical accuracy and language range '
        'is also well established, with confidence evident in this area. Although '
        'performance in connecting ideas logically and maintaining coherence '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'satisfactory', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in adapting tone and style appropriately to purpose, audience and '
        'context falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'satisfactory', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'satisfactory', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. Although '
        'performance in connecting ideas logically and maintaining coherence and in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'satisfactory', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context is also well established, with confidence evident in this area. '
        'Although performance in connecting ideas logically and maintaining coherence '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'satisfactory', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'Although performance in connecting ideas logically and maintaining coherence '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'needs_work', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'However, performance in grammatical accuracy and language range and in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context is still developing and requires further consolidation to reach the '
        'minimum expected standard for this level. However, performance in grammatical '
        'accuracy and language range falls well below the minimum expected standard for '
        'this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level. '
        'However, performance in grammatical accuracy and language range falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'confident', 'needs_work', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context, with confidence evident across '
        'these areas. However, performance in grammatical accuracy and language range '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'confident', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence is also well established, with confidence evident in '
        'this area. However, performance in grammatical accuracy and language range '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'confident', 'developing', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in grammatical accuracy and language range is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level. However, performance in adapting tone and style appropriately to '
        'purpose, audience and context falls well below the minimum expected standard '
        'for this level and requires substantial further development.'
    ),
    ('strong', 'confident', 'developing', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in grammatical accuracy and language range and in adapting tone '
        'and style appropriately to purpose, audience and context is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'confident', 'developing', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in adapting tone and style appropriately to purpose, audience and '
        'context satisfactorily meets the minimum expected standard for this level. '
        'Performance in grammatical accuracy and language range is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'confident', 'developing', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context, with confidence evident across '
        'these areas. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'confident', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence is also well established, with confidence evident in '
        'this area. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'confident', 'satisfactory', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in grammatical accuracy and language range satisfactorily meets '
        'the minimum expected standard for this level. However, performance in adapting '
        'tone and style appropriately to purpose, audience and context falls well below '
        'the minimum expected standard for this level and requires substantial further '
        'development.'
    ),
    ('strong', 'confident', 'satisfactory', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Performance in grammatical accuracy and language range satisfactorily meets '
        'the minimum expected standard for this level. Performance in adapting tone and '
        'style appropriately to purpose, audience and context is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'confident', 'satisfactory', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance in connecting ideas logically and maintaining '
        'coherence is also well established, with confidence evident in this area. '
        'Although performance in grammatical accuracy and language range and in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'confident', 'satisfactory', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in adapting tone and style '
        'appropriately to purpose, audience and context, with confidence evident across '
        'these areas. Although performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance in connecting ideas logically and '
        'maintaining coherence is also well established, with confidence evident in '
        'this area. Although performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'confident', 'needs_work'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in grammatical accuracy and language '
        'range, with confidence evident across these areas. However, performance in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'confident', 'confident', 'developing'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in grammatical accuracy and language '
        'range, with confidence evident across these areas. Performance in adapting '
        'tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'confident', 'confident', 'satisfactory'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in grammatical accuracy and language '
        'range, with confidence evident across these areas. Although performance in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'confident', 'confident'): (
        "{learner_name}'s ability to organise and present written work clearly is "
        'particularly strong. Performance is also well established in connecting ideas '
        'logically and maintaining coherence, in grammatical accuracy and language '
        'range, and in adapting tone and style appropriately to purpose, audience and '
        'context, with confidence evident across these areas.'
    ),
    ('strong', 'confident', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in adapting tone and style appropriately to purpose, '
        'audience and context. Performance is also well established in connecting ideas '
        'logically and maintaining coherence and in grammatical accuracy and language '
        'range, with confidence evident across these areas.'
    ),
    ('strong', 'confident', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence is also '
        'well established, with confidence evident in this area. However, performance '
        'in adapting tone and style appropriately to purpose, audience and context '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'confident', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence is also '
        'well established, with confidence evident in this area. Performance in '
        'adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'confident', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance in connecting ideas logically and maintaining coherence is also '
        'well established, with confidence evident in this area. Although performance '
        'in adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'confident', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in grammatical accuracy and language range. '
        'Performance is also well established in connecting ideas logically and '
        'maintaining coherence and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across these areas.'
    ),
    ('strong', 'confident', 'strong', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in grammatical accuracy and language range, and in '
        'adapting tone and style appropriately to purpose, audience and context. '
        'Performance in connecting ideas logically and maintaining coherence is also '
        'well established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'needs_work', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. However, performance in grammatical accuracy and language range and '
        'in adapting tone and style appropriately to purpose, audience and context '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in adapting tone and style appropriately to purpose, '
        'audience and context is still developing and requires further consolidation to '
        'reach the minimum expected standard for this level. However, performance in '
        'grammatical accuracy and language range falls well below the minimum expected '
        'standard for this level and requires substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in adapting tone and style appropriately to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. However, performance in grammatical accuracy and language range '
        'falls well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in adapting tone and style appropriately to purpose, '
        'audience and context is also well established, with confidence evident in this '
        'area. However, performance in grammatical accuracy and language range falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'strong', 'needs_work', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in adapting tone and style appropriately to purpose, audience and context. '
        'However, performance in grammatical accuracy and language range falls well '
        'below the minimum expected standard for this level and requires substantial '
        'further development.'
    ),
    ('strong', 'strong', 'developing', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level. However, performance in adapting tone and style '
        'appropriately to purpose, audience and context falls well below the minimum '
        'expected standard for this level and requires substantial further development.'
    ),
    ('strong', 'strong', 'developing', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range and in '
        'adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'strong', 'developing', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in adapting tone and style appropriately to purpose, '
        'audience and context satisfactorily meets the minimum expected standard for '
        'this level. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'strong', 'developing', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in adapting tone and style appropriately to purpose, '
        'audience and context is also well established, with confidence evident in this '
        'area. Performance in grammatical accuracy and language range is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'strong', 'developing', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in adapting tone and style appropriately to purpose, audience and context. '
        'Performance in grammatical accuracy and language range is still developing and '
        'requires further consolidation to reach the minimum expected standard for this '
        'level.'
    ),
    ('strong', 'strong', 'satisfactory', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. However, '
        'performance in adapting tone and style appropriately to purpose, audience and '
        'context falls well below the minimum expected standard for this level and '
        'requires substantial further development.'
    ),
    ('strong', 'strong', 'satisfactory', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level. Performance '
        'in adapting tone and style appropriately to purpose, audience and context is '
        'still developing and requires further consolidation to reach the minimum '
        'expected standard for this level.'
    ),
    ('strong', 'strong', 'satisfactory', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Although performance in grammatical accuracy and language range and '
        'in adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in these areas.'
    ),
    ('strong', 'strong', 'satisfactory', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in adapting tone and style appropriately to purpose, '
        'audience and context is also well established, with confidence evident in this '
        'area. Although performance in grammatical accuracy and language range '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'strong', 'satisfactory', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in adapting tone and style appropriately to purpose, audience and context. '
        'Although performance in grammatical accuracy and language range satisfactorily '
        'meets the minimum expected standard for this level, there is still scope for '
        'further development and consolidation in this area.'
    ),
    ('strong', 'strong', 'confident', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range is also well '
        'established, with confidence evident in this area. However, performance in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'strong', 'confident', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range is also well '
        'established, with confidence evident in this area. Performance in adapting '
        'tone and style appropriately to purpose, audience and context is still '
        'developing and requires further consolidation to reach the minimum expected '
        'standard for this level.'
    ),
    ('strong', 'strong', 'confident', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance in grammatical accuracy and language range is also well '
        'established, with confidence evident in this area. Although performance in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'strong', 'confident', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly and in connecting ideas logically and maintaining '
        'coherence. Performance is also well established in grammatical accuracy and '
        'language range and in adapting tone and style appropriately to purpose, '
        'audience and context, with confidence evident across these areas.'
    ),
    ('strong', 'strong', 'confident', 'strong'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in adapting tone and style appropriately to purpose, audience and context. '
        'Performance in grammatical accuracy and language range is also well '
        'established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'strong', 'needs_work'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in grammatical accuracy and language range. However, performance in '
        'adapting tone and style appropriately to purpose, audience and context falls '
        'well below the minimum expected standard for this level and requires '
        'substantial further development.'
    ),
    ('strong', 'strong', 'strong', 'developing'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in grammatical accuracy and language range. Performance in adapting tone '
        'and style appropriately to purpose, audience and context is still developing '
        'and requires further consolidation to reach the minimum expected standard for '
        'this level.'
    ),
    ('strong', 'strong', 'strong', 'satisfactory'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in grammatical accuracy and language range. Although performance in '
        'adapting tone and style appropriately to purpose, audience and context '
        'satisfactorily meets the minimum expected standard for this level, there is '
        'still scope for further development and consolidation in this area.'
    ),
    ('strong', 'strong', 'strong', 'confident'): (
        '{learner_name} demonstrates particular strengths in organising and presenting '
        'written work clearly, in connecting ideas logically and maintaining coherence, '
        'and in grammatical accuracy and language range. Performance in adapting tone '
        'and style appropriately to purpose, audience and context is also well '
        'established, with confidence evident in this area.'
    ),
    ('strong', 'strong', 'strong', 'strong'): (
        "{learner_name}'s written communication is particularly strong across all four "
        'assessed areas. Organisation and clear presentation, cohesion, grammatical '
        'accuracy and language range, and control of register are all particular '
        'strengths at this level.'
    ),
}
