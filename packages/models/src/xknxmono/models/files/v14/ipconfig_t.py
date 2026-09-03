from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.ipconfig_assign_t import IpconfigAssign

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class Ipconfig:
    class Meta:
        name = "IPConfig_t"

    assign: IpconfigAssign = field(
        default=IpconfigAssign.AUTO,
        metadata={
            "name": "Assign",
            "type": "Attribute",
        },
    )
    ipaddress: None | str = field(
        default=None,
        metadata={
            "name": "IPAddress",
            "type": "Attribute",
            "pattern": r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    subnet_mask: None | str = field(
        default=None,
        metadata={
            "name": "SubnetMask",
            "type": "Attribute",
            "pattern": r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    default_gateway: None | str = field(
        default=None,
        metadata={
            "name": "DefaultGateway",
            "type": "Attribute",
            "pattern": r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    macaddress: None | str = field(
        default=None,
        metadata={
            "name": "MACAddress",
            "type": "Attribute",
            "max_length": 50,
        },
    )
