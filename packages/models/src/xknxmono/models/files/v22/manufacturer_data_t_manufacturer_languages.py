from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.language_data_t import LanguageData

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerLanguages:
    class Meta:
        global_type = False

    language: list[LanguageData] = field(
        default_factory=list,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
