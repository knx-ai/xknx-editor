from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_bus_interfaces_bus_interface_access_type import (
    ApplicationProgramStaticBusInterfacesBusInterfaceAccessType,
)


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticBusInterfacesBusInterface:
    """
    :ivar id: registration-relevant
    :ivar address_index: registration-relevant
    :ivar access_type: registration-relevant
    :ivar text:
    """

    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    address_index: int = field(
        metadata={
            "name": "AddressIndex",
            "type": "Attribute",
        }
    )
    access_type: ApplicationProgramStaticBusInterfacesBusInterfaceAccessType = field(
        metadata={
            "name": "AccessType",
            "type": "Attribute",
        }
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
