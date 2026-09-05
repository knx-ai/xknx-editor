from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class GroupAddress:
    class Meta:
        name = "GroupAddress_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 65535,
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    unfiltered: bool = field(
        default=False,
        metadata={
            "name": "Unfiltered",
            "type": "Attribute",
        },
    )
    central: bool = field(
        default=False,
        metadata={
            "name": "Central",
            "type": "Attribute",
        },
    )
    global_value: bool = field(
        default=False,
        metadata={
            "name": "Global",
            "type": "Attribute",
        },
    )
    datapoint_type: list[str] = field(
        default_factory=list,
        metadata={
            "name": "DatapointType",
            "type": "Attribute",
            "tokens": True,
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
