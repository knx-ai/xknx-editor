from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeRestrictionEnumeration:
    """
    :ivar text:
    :ivar value: registration-relevant
    :ivar id: registration-relevant
    :ivar display_order:
    :ivar binary_value: registration-relevant
    """

    class Meta:
        global_type = False

    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    value: int = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    display_order: None | int = field(
        default=None,
        metadata={
            "name": "DisplayOrder",
            "type": "Attribute",
        },
    )
    binary_value: None | bytes = field(
        default=None,
        metadata={
            "name": "BinaryValue",
            "type": "Attribute",
            "format": "base64",
        },
    )
