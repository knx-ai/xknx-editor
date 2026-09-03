from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.application_program_static_t_bus_interfaces_bus_interface import (
    ApplicationProgramStaticBusInterfacesBusInterface,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticBusInterfaces:
    class Meta:
        global_type = False

    bus_interface: list[ApplicationProgramStaticBusInterfacesBusInterface] = field(
        default_factory=list,
        metadata={
            "name": "BusInterface",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
