from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.access_t import Access
from xknxmono.models.files.v23.button_t_event_handler_online import (
    ButtonEventHandlerOnline,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class Button:
    """
    :ivar id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar access:
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    :ivar cell:
    :ivar icon:
    :ivar event_handler: registration-relevant
    :ivar event_handler_parameters: registration-relevant
    :ivar event_handler_online: registration-relevant
    """

    class Meta:
        name = "Button_t"

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
    event_handler: None | str = field(
        default=None,
        metadata={
            "name": "EventHandler",
            "type": "Attribute",
        },
    )
    event_handler_parameters: None | str = field(
        default=None,
        metadata={
            "name": "EventHandlerParameters",
            "type": "Attribute",
        },
    )
    event_handler_online: None | ButtonEventHandlerOnline = field(
        default=None,
        metadata={
            "name": "EventHandlerOnline",
            "type": "Attribute",
        },
    )
