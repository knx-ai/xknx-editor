from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_bus_interfaces_bus_interface import (
    ApplicationProgramStaticBusInterfacesBusInterface,
)


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticBusInterfaces:
    class Meta:
        global_type = False

    bus_interface: list[ApplicationProgramStaticBusInterfacesBusInterface] = field(
        default_factory=list,
        metadata={
            "name": "BusInterface",
            "type": "Element",
        },
    )
