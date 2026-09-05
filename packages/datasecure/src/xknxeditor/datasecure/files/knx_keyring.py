from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://knx.org/xml/keyring/1"


@dataclass(slots=True, kw_only=True)
class Backbone:
    class Meta:
        namespace = "http://knx.org/xml/keyring/1"

    multicast_address: str = field(
        metadata={
            "name": "MulticastAddress",
            "type": "Attribute",
            "pattern": r"2(2[4-9]|3[0-9])\.((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        }
    )
    latency: None | int = field(
        default=None,
        metadata={
            "name": "Latency",
            "type": "Attribute",
            "max_inclusive": 8000,
        },
    )
    key: None | str = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Attribute",
            "pattern": r"[A-Za-z0-9\+/]{21}[AQgw]==",
        },
    )


@dataclass(slots=True, kw_only=True)
class Devices:
    class Meta:
        namespace = "http://knx.org/xml/keyring/1"

    device: list[Devices.Device] = field(
        default_factory=list,
        metadata={
            "name": "Device",
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(slots=True, kw_only=True)
    class Device:
        individual_address: str = field(
            metadata={
                "name": "IndividualAddress",
                "type": "Attribute",
                "pattern": r"((1[0-5]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
            }
        )
        tool_key: None | str = field(
            default=None,
            metadata={
                "name": "ToolKey",
                "type": "Attribute",
                "pattern": r"[A-Za-z0-9\+/]{21}[AQgw]==",
            },
        )
        sequence_number: None | int = field(
            default=None,
            metadata={
                "name": "SequenceNumber",
                "type": "Attribute",
            },
        )
        management_password: None | str = field(
            default=None,
            metadata={
                "name": "ManagementPassword",
                "type": "Attribute",
                "pattern": r"[A-Za-z0-9\+/]{42}[AEIMQUYcgkosw048]=",
            },
        )
        authentication: None | str = field(
            default=None,
            metadata={
                "name": "Authentication",
                "type": "Attribute",
                "pattern": r"[A-Za-z0-9\+/]{42}[AEIMQUYcgkosw048]=",
            },
        )
        fdsk: None | str = field(
            default=None,
            metadata={
                "name": "FDSK",
                "type": "Attribute",
                "pattern": r"[A-Za-z0-9\+/]{21}[AQgw]==",
            },
        )
        password: None | bytes = field(
            default=None,
            metadata={
                "name": "Password",
                "type": "Attribute",
                "format": "base64",
            },
        )
        serial_number: None | str = field(
            default=None,
            metadata={
                "name": "SerialNumber",
                "type": "Attribute",
            },
        )


@dataclass(slots=True, kw_only=True)
class GroupAddresses:
    class Meta:
        namespace = "http://knx.org/xml/keyring/1"

    group: list[GroupAddresses.Group] = field(
        default_factory=list,
        metadata={
            "name": "Group",
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(slots=True, kw_only=True)
    class Group:
        address: int = field(
            metadata={
                "name": "Address",
                "type": "Attribute",
            }
        )
        key: str = field(
            metadata={
                "name": "Key",
                "type": "Attribute",
                "pattern": r"[A-Za-z0-9\+/]{21}[AQgw]==",
            }
        )


class InterfaceType(Enum):
    BACKBONE = "Backbone"
    TUNNELING = "Tunneling"
    USB = "USB"
    INTERNAL = "Internal"


@dataclass(slots=True, kw_only=True)
class Interface:
    class Meta:
        namespace = "http://knx.org/xml/keyring/1"

    group: list[Interface.Group] = field(
        default_factory=list,
        metadata={
            "name": "Group",
            "type": "Element",
        },
    )
    type_value: InterfaceType = field(
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    host: None | str = field(
        default=None,
        metadata={
            "name": "Host",
            "type": "Attribute",
            "pattern": r"((1[0-5]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    individual_address: None | str = field(
        default=None,
        metadata={
            "name": "IndividualAddress",
            "type": "Attribute",
            "pattern": r"((1[0-5]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    user_id: None | int = field(
        default=None,
        metadata={
            "name": "UserID",
            "type": "Attribute",
        },
    )
    password: None | str = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Attribute",
            "pattern": r"[A-Za-z0-9\+/]{42}[AEIMQUYcgkosw048]=",
        },
    )
    authentication: None | str = field(
        default=None,
        metadata={
            "name": "Authentication",
            "type": "Attribute",
            "pattern": r"[A-Za-z0-9\+/]{42}[AEIMQUYcgkosw048]=",
        },
    )

    @dataclass(slots=True, kw_only=True)
    class Group:
        address: int = field(
            metadata={
                "name": "Address",
                "type": "Attribute",
            }
        )
        senders: list[str] = field(
            default_factory=list,
            metadata={
                "name": "Senders",
                "type": "Attribute",
                "pattern": r"((1[0-5]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
                "tokens": True,
            },
        )
        rx_rf_multi_fast: None | int = field(
            default=None,
            metadata={
                "name": "RxRfMultiFast",
                "type": "Attribute",
            },
        )
        rx_rf_multi_slow: None | int = field(
            default=None,
            metadata={
                "name": "RxRfMultiSlow",
                "type": "Attribute",
            },
        )
        tx_rf_ready: bool = field(
            default=False,
            metadata={
                "name": "TxRfReady",
                "type": "Attribute",
            },
        )
        tx_rf_multi_fast: list[int] = field(
            default_factory=list,
            metadata={
                "name": "TxRfMultiFast",
                "type": "Attribute",
                "tokens": True,
            },
        )
        tx_rf_multi_slow: list[int] = field(
            default_factory=list,
            metadata={
                "name": "TxRfMultiSlow",
                "type": "Attribute",
                "tokens": True,
            },
        )


@dataclass(slots=True, kw_only=True)
class Keyring:
    class Meta:
        namespace = "http://knx.org/xml/keyring/1"

    backbone: None | Backbone = field(
        default=None,
        metadata={
            "name": "Backbone",
            "type": "Element",
        },
    )
    interface: list[Interface] = field(
        default_factory=list,
        metadata={
            "name": "Interface",
            "type": "Element",
        },
    )
    group_addresses: None | GroupAddresses = field(
        default=None,
        metadata={
            "name": "GroupAddresses",
            "type": "Element",
        },
    )
    devices: None | Devices = field(
        default=None,
        metadata={
            "name": "Devices",
            "type": "Element",
        },
    )
    project: str = field(
        metadata={
            "name": "Project",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    created: XmlDateTime = field(
        metadata={
            "name": "Created",
            "type": "Attribute",
        }
    )
    created_by: str = field(
        metadata={
            "name": "CreatedBy",
            "type": "Attribute",
        }
    )
    signature: str = field(
        metadata={
            "name": "Signature",
            "type": "Attribute",
            "pattern": r"[A-Za-z0-9\+/]{21}[AQgw]==",
        }
    )
