from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.access_t import Access
from xknxmono.models.intermediate.parameter_separator_t_uihint import (
    ParameterSeparatorUihint,
)
from xknxmono.models.intermediate.text_alignment_t import TextAlignment


@dataclass(slots=True, kw_only=True)
class ParameterSeparator:
    """
    :ivar id: registration-relevant
    :ivar text:
    :ivar access:
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    :ivar uihint:
    :ivar cell:
    :ivar icon:
    :ivar name:
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
    uihint: None | ParameterSeparatorUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
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
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    text_alignment: None | TextAlignment = field(
        default=None,
        metadata={
            "name": "TextAlignment",
            "type": "Attribute",
        },
    )
