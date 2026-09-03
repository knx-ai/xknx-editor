from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.access_t import Access

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ParameterSeparator:
    """
    :ivar id: registration-relevant
    :ivar text:
    :ivar access:
    :ivar horizontal_ruler:
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    """

    class Meta:
        name = "ParameterSeparator_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    access: Access = field(
        default=Access.READ_WRITE,
        metadata={
            "name": "Access",
            "type": "Attribute",
        },
    )
    horizontal_ruler: bool = field(
        default=False,
        metadata={
            "name": "HorizontalRuler",
            "type": "Attribute",
        },
    )
    text_parameter_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "TextParameterRefId",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
