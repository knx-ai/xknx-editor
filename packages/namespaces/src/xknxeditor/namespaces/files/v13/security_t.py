from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class Security:
    class Meta:
        name = "Security_t"

    loaded_iprouting_backbone_key: None | str = field(
        default=None,
        metadata={
            "name": "LoadedIPRoutingBackboneKey",
            "type": "Attribute",
            "max_length": 40,
        },
    )
    device_authentication_code: None | str = field(
        default=None,
        metadata={
            "name": "DeviceAuthenticationCode",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    loaded_device_authentication_code: None | str = field(
        default=None,
        metadata={
            "name": "LoadedDeviceAuthenticationCode",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    device_management_password: None | str = field(
        default=None,
        metadata={
            "name": "DeviceManagementPassword",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    loaded_device_management_password: None | str = field(
        default=None,
        metadata={
            "name": "LoadedDeviceManagementPassword",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    tool_key: None | str = field(
        default=None,
        metadata={
            "name": "ToolKey",
            "type": "Attribute",
            "max_length": 40,
        },
    )
    loaded_tool_key: None | str = field(
        default=None,
        metadata={
            "name": "LoadedToolKey",
            "type": "Attribute",
            "max_length": 40,
        },
    )
    sequence_number: None | int = field(
        default=None,
        metadata={
            "name": "SequenceNumber",
            "type": "Attribute",
        },
    )
    sequence_number_timestamp: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "SequenceNumberTimestamp",
            "type": "Attribute",
        },
    )
