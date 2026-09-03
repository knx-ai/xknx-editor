from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.language_data_t_translation_unit_translation_element_translation import (
    LanguageDataTranslationUnitTranslationElementTranslation,
)


@dataclass(slots=True, kw_only=True)
class LanguageDataTranslationUnitTranslationElement:
    class Meta:
        global_type = False

    translation: list[LanguageDataTranslationUnitTranslationElementTranslation] = field(
        default_factory=list,
        metadata={
            "name": "Translation",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
