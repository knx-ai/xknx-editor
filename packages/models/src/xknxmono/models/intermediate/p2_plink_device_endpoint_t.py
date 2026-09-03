from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.p2_plink_endpoint_t import P2PlinkEndpoint


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
