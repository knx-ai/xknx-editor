from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class DeviceCertificate:
    class Meta:
        name = "DeviceCertificate_t"

    serial_number: bytes = field(
        metadata={
            "name": "SerialNumber",
            "type": "Attribute",
            "format": "base64",
        }
    )
    fdsk: None | str = field(
        default=None,
        metadata={
            "name": "FDSK",
            "type": "Attribute",
            "max_length": 100,
        },
    )
    password: None | str = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Attribute",
        },
    )
