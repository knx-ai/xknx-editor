from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.group_addresses_t_group_ranges import (
    GroupAddressesGroupRanges,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class GroupAddresses:
    class Meta:
        name = "GroupAddresses_t"

    group_ranges: GroupAddressesGroupRanges = field(
        metadata={
            "name": "GroupRanges",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        }
    )
