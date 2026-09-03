from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.bus_interface_t import BusInterface


@dataclass(slots=True, kw_only=True)
class DeviceInstanceBusInterfaces:
    class Meta:
        global_type = False

    bus_interface: list[BusInterface] = field(
        default_factory=list,
        metadata={
            "name": "BusInterface",
            "type": "Element",
        },
    )
