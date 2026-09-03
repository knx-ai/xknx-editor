from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.master_data_t_product_languages_language import (
    MasterDataProductLanguagesLanguage,
)


@dataclass(slots=True, kw_only=True)
class MasterDataProductLanguages:
    class Meta:
        global_type = False

    language: list[MasterDataProductLanguagesLanguage] = field(
        default_factory=list,
        metadata={
            "name": "Language",
            "type": "Element",
        },
    )
