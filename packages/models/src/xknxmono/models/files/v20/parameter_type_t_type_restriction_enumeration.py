from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.horizontal_alignment_t import HorizontalAlignment

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeRestrictionEnumeration:
    """
    :ivar text:
    :ivar icon:
    :ivar picture_alignment:
    :ivar value: registration-relevant
    :ivar id: registration-relevant
    :ivar display_order:
    :ivar binary_value: registration-relevant
    """

    class Meta:
        global_type = False

    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    icon: None | str = field(
        default=None,
        metadata={
            "name": "Icon",
            "type": "Attribute",
        },
    )
    picture_alignment: HorizontalAlignment = field(
        default=HorizontalAlignment.LEFT,
        metadata={
            "name": "PictureAlignment",
            "type": "Attribute",
        },
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
