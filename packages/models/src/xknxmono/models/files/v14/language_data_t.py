from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.language_data_t_translation_unit import (
    LanguageDataTranslationUnit,
)

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class LanguageData:
    class Meta:
        name = "LanguageData_t"

    translation_unit: list[LanguageDataTranslationUnit] = field(
        default_factory=list,
        metadata={
            "name": "TranslationUnit",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
    identifier: str = field(
        metadata={
            "name": "Identifier",
            "type": "Attribute",
        }
    )
