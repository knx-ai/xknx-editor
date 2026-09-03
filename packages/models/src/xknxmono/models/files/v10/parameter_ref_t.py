from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.access_t import Access

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ParameterRef:
    """
    :ivar id: registration-relevant
    :ivar ref_id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar tag:
    :ivar display_order:
    :ivar access:
    :ivar value: registration-relevant
    """

    class Meta:
        name = "ParameterRef_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    tag: None | str = field(
        default=None,
        metadata={
            "name": "Tag",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    display_order: None | int = field(
        default=None,
        metadata={
            "name": "DisplayOrder",
            "type": "Attribute",
        },
    )
    access: None | Access = field(
        default=None,
        metadata={
            "name": "Access",
            "type": "Attribute",
        },
    )
    value: None | str = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        },
    )
