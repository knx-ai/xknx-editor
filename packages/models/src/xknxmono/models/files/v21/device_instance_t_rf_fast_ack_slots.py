from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.device_instance_t_rf_fast_ack_slots_slot import (
    DeviceInstanceRfFastAckSlotsSlot,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceRfFastAckSlots:
    class Meta:
        global_type = False

    slot: list[DeviceInstanceRfFastAckSlotsSlot] = field(
        default_factory=list,
        metadata={
            "name": "Slot",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
