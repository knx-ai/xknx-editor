from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.language_data_t import LanguageData

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class MasterDataLanguages:
    class Meta:
        global_type = False

    language: list[LanguageData] = field(
        default_factory=list,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
