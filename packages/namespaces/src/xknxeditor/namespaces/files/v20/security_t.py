from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class Security:
    class Meta:
        name = "Security_t"

    loaded_iprouting_backbone_key: None | str = field(
        default=None,
        metadata={
            "name": "LoadedIPRoutingBackboneKey",
            "type": "Attribute",
            "max_length": 100,
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
    device_authentication_code_hash: None | bytes = field(
        default=None,
        metadata={
            "name": "DeviceAuthenticationCodeHash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    loaded_device_authentication_code_hash: None | bytes = field(
        default=None,
        metadata={
            "name": "LoadedDeviceAuthenticationCodeHash",
            "type": "Attribute",
            "format": "base64",
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
    device_management_password_hash: None | bytes = field(
        default=None,
        metadata={
            "name": "DeviceManagementPasswordHash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    loaded_device_management_password_hash: None | bytes = field(
        default=None,
        metadata={
            "name": "LoadedDeviceManagementPasswordHash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    tool_key: None | str = field(
        default=None,
        metadata={
            "name": "ToolKey",
            "type": "Attribute",
            "max_length": 100,
        },
    )
    loaded_tool_key: None | str = field(
        default=None,
        metadata={
            "name": "LoadedToolKey",
            "type": "Attribute",
            "max_length": 100,
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
