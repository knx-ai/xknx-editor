from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.device_instance_t import DeviceInstance


@dataclass(slots=True, kw_only=True)
class TopologyUnassignedDevices:
    class Meta:
        global_type = False

    device_instance: list[DeviceInstance] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstance",
            "type": "Element",
        },
    )
