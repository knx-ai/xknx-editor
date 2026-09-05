from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ChannelInstance:
    class Meta:
        name = "ChannelInstance_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    ref_id: None | str = field(
        default=None,
        metadata={
            "name": "RefId",
            "type": "Attribute",
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
            "max_length": 255,
        },
    )
    is_active: None | bool = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Attribute",
        },
    )
    context: None | str = field(
        default=None,
        metadata={
            "name": "Context",
            "type": "Attribute",
        },
    )
