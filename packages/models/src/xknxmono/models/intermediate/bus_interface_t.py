from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.bus_interface_t_connectors import (
    BusInterfaceConnectors,
)


@dataclass(slots=True, kw_only=True)
class BusInterface:
    class Meta:
        name = "BusInterface_t"

    connectors: None | BusInterfaceConnectors = field(
        default=None,
        metadata={
            "name": "Connectors",
            "type": "Element",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    password: None | str = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    password_hash: None | bytes = field(
        default=None,
        metadata={
            "name": "PasswordHash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    is_secure_enabled: bool = field(
        default=True,
        metadata={
            "name": "IsSecureEnabled",
            "type": "Attribute",
        },
    )
