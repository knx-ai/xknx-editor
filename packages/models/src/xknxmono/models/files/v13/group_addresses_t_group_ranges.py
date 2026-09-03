from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.group_range_t import GroupRange

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class GroupAddressesGroupRanges:
    class Meta:
        global_type = False

    group_range: list[GroupRange] = field(
        default_factory=list,
        metadata={
            "name": "GroupRange",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "max_occurs": 65535,
        },
    )
