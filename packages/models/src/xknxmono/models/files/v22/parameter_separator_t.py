from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.access_t import Access
from xknxmono.models.files.v22.parameter_separator_t_uihint import (
    ParameterSeparatorUihint,
)
from xknxmono.models.files.v22.text_alignment_t import TextAlignment

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ParameterSeparator:
    """
    :ivar id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar access:
    :ivar uihint:
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    :ivar cell:
    :ivar icon:
    :ivar text_alignment:
    """

    class Meta:
        name = "ParameterSeparator_t"

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
    uihint: None | ParameterSeparatorUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
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
    cell: None | str = field(
        default=None,
        metadata={
            "name": "Cell",
            "type": "Attribute",
            "pattern": r"\d+,\d+",
        },
    )
    icon: None | str = field(
        default=None,
        metadata={
            "name": "Icon",
            "type": "Attribute",
        },
    )
    text_alignment: None | TextAlignment = field(
        default=None,
        metadata={
            "name": "TextAlignment",
            "type": "Attribute",
        },
    )
