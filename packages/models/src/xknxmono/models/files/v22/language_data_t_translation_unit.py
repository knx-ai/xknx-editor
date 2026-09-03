from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.language_data_t_translation_unit_translation_element import (
    LanguageDataTranslationUnitTranslationElement,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class LanguageDataTranslationUnit:
    class Meta:
        global_type = False

    translation_element: list[LanguageDataTranslationUnitTranslationElement] = field(
        default_factory=list,
        metadata={
            "name": "TranslationElement",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    version: int = field(
        default=0,
        metadata={
            "name": "Version",
            "type": "Attribute",
        },
    )
