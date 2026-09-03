from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.group_range_t import GroupRange


@dataclass(slots=True, kw_only=True)
class GroupAddressesGroupRanges:
    class Meta:
        global_type = False

    group_range: list[GroupRange] = field(
        default_factory=list,
        metadata={
            "name": "GroupRange",
            "type": "Element",
            "max_occurs": 65535,
        },
    )
