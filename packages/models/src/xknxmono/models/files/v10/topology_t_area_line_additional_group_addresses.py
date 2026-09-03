from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.topology_t_area_line_additional_group_addresses_group_address import (
    TopologyAreaLineAdditionalGroupAddressesGroupAddress,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class TopologyAreaLineAdditionalGroupAddresses:
    class Meta:
        global_type = False

    group_address: list[TopologyAreaLineAdditionalGroupAddressesGroupAddress] = field(
        default_factory=list,
        metadata={
            "name": "GroupAddress",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
