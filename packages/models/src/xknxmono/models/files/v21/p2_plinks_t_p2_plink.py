from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.p2_plink_bus_interface_endpoint_t import (
    P2PlinkBusInterfaceEndpoint,
)
from xknxmono.models.files.v21.p2_plink_device_endpoint_t import P2PlinkDeviceEndpoint

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class P2PlinksP2Plink:
    class Meta:
        global_type = False

    choice: list[P2PlinkDeviceEndpoint | P2PlinkBusInterfaceEndpoint] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DeviceEndpoint",
                    "type": P2PlinkDeviceEndpoint,
                    "namespace": "http://knx.org/xml/project/21",
                    "max_occurs": 2,
                },
                {
                    "name": "BusInterfaceEndpoint",
                    "type": P2PlinkBusInterfaceEndpoint,
                    "namespace": "http://knx.org/xml/project/21",
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
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
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
    key: None | str = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Attribute",
            "max_length": 100,
        },
    )
