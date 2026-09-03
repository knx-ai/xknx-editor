from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.bus_interface_t import BusInterface

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceBusInterfaces:
    class Meta:
        global_type = False

    bus_interface: list[BusInterface] = field(
        default_factory=list,
        metadata={
            "name": "BusInterface",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
