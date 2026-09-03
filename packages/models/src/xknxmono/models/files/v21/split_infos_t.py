from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.split_info_t import SplitInfo

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class SplitInfos:
    class Meta:
        name = "SplitInfos_t"

    split_info: list[SplitInfo] = field(
        default_factory=list,
        metadata={
            "name": "SplitInfo",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
