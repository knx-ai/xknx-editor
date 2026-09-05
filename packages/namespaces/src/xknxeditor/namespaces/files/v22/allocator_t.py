from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class Allocator:
    """
    :ivar id:
    :ivar name: registration-relevant
    :ivar internal_description:
    :ivar start: registration-relevant
    :ivar max_inclusive: registration-relevant
    :ivar error_message_ref:
    """

    class Meta:
        name = "Allocator_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    start: int = field(
        metadata={
            "name": "Start",
            "type": "Attribute",
        }
    )
    max_inclusive: int = field(
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
        }
    )
    error_message_ref: None | str = field(
        default=None,
        metadata={
            "name": "ErrorMessageRef",
            "type": "Attribute",
        },
    )
