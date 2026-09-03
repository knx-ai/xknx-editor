from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.topology_t_area_line_segment_additional_group_addresses_group_address import (
    TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class TopologyAreaLineSegmentAdditionalGroupAddresses:
    class Meta:
        global_type = False

    group_address: list[TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress] = (
        field(
            default_factory=list,
            metadata={
                "name": "GroupAddress",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/21",
                "min_occurs": 1,
            },
        )
    )
