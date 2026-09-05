from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class DeviceInstanceRfFastAckSlotsSlot:
    class Meta:
        global_type = False

    group_address_ref_id: str = field(
        metadata={
            "name": "GroupAddressRefId",
            "type": "Attribute",
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
            "max_inclusive": 63,
        }
    )
