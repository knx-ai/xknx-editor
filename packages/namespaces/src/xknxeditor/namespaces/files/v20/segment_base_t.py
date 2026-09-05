from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class SegmentBase:
    """
    :ivar data: registration-relevant
    :ivar mask: registration-relevant
    :ivar id: registration-relevant
    :ivar name:
    :ivar size: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "SegmentBase_t"

    data: None | bytes = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "format": "base64",
        },
    )
    mask: None | bytes = field(
        default=None,
        metadata={
            "name": "Mask",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "format": "base64",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
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
    size: int = field(
        metadata={
            "name": "Size",
            "type": "Attribute",
            "max_inclusive": 1048575,
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
