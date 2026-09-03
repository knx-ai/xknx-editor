from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.p2_plink_endpoint_t import P2PlinkEndpoint

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class P2PlinkDeviceEndpoint(P2PlinkEndpoint):
    class Meta:
        name = "P2PLinkDeviceEndpoint_t"

    security_roles: list[str] = field(
        default_factory=list,
        metadata={
            "name": "SecurityRoles",
            "type": "Attribute",
            "tokens": True,
        },
    )
