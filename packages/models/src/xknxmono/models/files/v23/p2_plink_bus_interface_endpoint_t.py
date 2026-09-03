from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.p2_plink_endpoint_t import P2PlinkEndpoint

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class P2PlinkBusInterfaceEndpoint(P2PlinkEndpoint):
    class Meta:
        name = "P2PLinkBusInterfaceEndpoint_t"

    bus_interface_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "BusInterfaceRefId",
            "type": "Attribute",
        },
    )
