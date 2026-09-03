from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.split_info_t import SplitInfo


@dataclass(slots=True, kw_only=True)
class SplitInfos:
    class Meta:
        name = "SplitInfos_t"

    split_info: list[SplitInfo] = field(
        default_factory=list,
        metadata={
            "name": "SplitInfo",
            "type": "Element",
        },
    )
