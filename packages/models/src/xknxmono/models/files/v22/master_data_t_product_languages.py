from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.master_data_t_product_languages_language import (
    MasterDataProductLanguagesLanguage,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class MasterDataProductLanguages:
    class Meta:
        global_type = False

    language: list[MasterDataProductLanguagesLanguage] = field(
        default_factory=list,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
