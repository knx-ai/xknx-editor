from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.language_data_t_translation_unit import (
    LanguageDataTranslationUnit,
)


@dataclass(slots=True, kw_only=True)
class LanguageData:
    class Meta:
        name = "LanguageData_t"

    translation_unit: list[LanguageDataTranslationUnit] = field(
        default_factory=list,
        metadata={
            "name": "TranslationUnit",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    identifier: str = field(
        metadata={
            "name": "Identifier",
            "type": "Attribute",
        }
    )
