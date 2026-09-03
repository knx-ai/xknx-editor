from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ComObjectInstanceRefConnectorsReceive:
    class Meta:
        global_type = False

    group_address_ref_id: str = field(
        metadata={
            "name": "GroupAddressRefId",
            "type": "Attribute",
        }
    )
    acknowledge: bool = field(
        default=False,
        metadata={
            "name": "Acknowledge",
            "type": "Attribute",
        },
    )
