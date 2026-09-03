from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.bus_interface_t import BusInterface

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceBusInterfaces:
    class Meta:
        global_type = False

    bus_interface: list[BusInterface] = field(
        default_factory=list,
        metadata={
            "name": "BusInterface",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
