from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceAdditionalAddressesAddress:
    class Meta:
        global_type = False

    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 255,
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
