from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.device_instance_t_rf_fast_ack_slots_slot import (
    DeviceInstanceRfFastAckSlotsSlot,
)


@dataclass(slots=True, kw_only=True)
class DeviceInstanceRfFastAckSlots:
    class Meta:
        global_type = False

    slot: list[DeviceInstanceRfFastAckSlotsSlot] = field(
        default_factory=list,
        metadata={
            "name": "Slot",
            "type": "Element",
        },
    )
