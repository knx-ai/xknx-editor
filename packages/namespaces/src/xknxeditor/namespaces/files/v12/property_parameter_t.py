from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class PropertyParameter:
    """
    :ivar object_index: registration-relevant
    :ivar object_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar property_id: registration-relevant
    :ivar offset: registration-relevant
    :ivar bit_offset: registration-relevant
    """

    class Meta:
        name = "PropertyParameter_t"

    object_index: None | int = field(
        default=None,
        metadata={
            "name": "ObjectIndex",
            "type": "Attribute",
        },
    )
    object_type: None | int = field(
        default=None,
        metadata={
            "name": "ObjectType",
            "type": "Attribute",
        },
    )
    occurrence: int = field(
        default=0,
        metadata={
            "name": "Occurrence",
            "type": "Attribute",
        },
    )
    property_id: int = field(
        metadata={
            "name": "PropertyId",
            "type": "Attribute",
        }
    )
    offset: int = field(
        metadata={
            "name": "Offset",
            "type": "Attribute",
        }
    )
    bit_offset: int = field(
        metadata={
            "name": "BitOffset",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 7,
        }
    )
