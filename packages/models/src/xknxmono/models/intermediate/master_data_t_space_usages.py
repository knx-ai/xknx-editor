from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.space_usage_t import SpaceUsage


@dataclass(slots=True, kw_only=True)
class MasterDataSpaceUsages:
    class Meta:
        global_type = False

    space_usage: list[SpaceUsage] = field(
        default_factory=list,
        metadata={
            "name": "SpaceUsage",
            "type": "Element",
        },
    )
