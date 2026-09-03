from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.bus_interface_t_connectors import BusInterfaceConnectors

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class BusInterface:
    class Meta:
        name = "BusInterface_t"

    connectors: None | BusInterfaceConnectors = field(
        default=None,
        metadata={
            "name": "Connectors",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
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
