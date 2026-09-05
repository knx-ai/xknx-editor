from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class BusInterfaceConnectorsConnector:
    class Meta:
        global_type = False

    group_address_ref_id: str = field(
        metadata={
            "name": "GroupAddressRefId",
            "type": "Attribute",
        }
    )
