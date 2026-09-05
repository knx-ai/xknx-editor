from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class P2PlinkEndpoint:
    class Meta:
        name = "P2PLinkEndpoint_t"

    device_ref_id: str = field(
        metadata={
            "name": "DeviceRefId",
            "type": "Attribute",
        }
    )
