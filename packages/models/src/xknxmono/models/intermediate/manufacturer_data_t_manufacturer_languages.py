from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.language_data_t import LanguageData


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerLanguages:
    class Meta:
        global_type = False

    language: list[LanguageData] = field(
        default_factory=list,
        metadata={
            "name": "Language",
            "type": "Element",
            "min_occurs": 1,
        },
    )
