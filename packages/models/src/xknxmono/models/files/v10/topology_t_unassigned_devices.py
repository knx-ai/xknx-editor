from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.device_instance_t import DeviceInstance

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class TopologyUnassignedDevices:
    class Meta:
        global_type = False

    device_instance: list[DeviceInstance] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstance",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
