from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.com_object_priority_t import ComObjectPriority
from xknxmono.models.files.v10.com_object_size_t import ComObjectSize
from xknxmono.models.files.v10.enable_t import Enable

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ComObjectRef:
    """
    :ivar id: registration-relevant
    :ivar ref_id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar tag:
    :ivar function_text:
    :ivar visible_description:
    :ivar priority:
    :ivar object_size: registration-relevant
    :ivar read_flag:
    :ivar write_flag:
    :ivar communication_flag:
    :ivar transmit_flag:
    :ivar update_flag:
    :ivar read_on_init_flag:
    :ivar datapoint_type:
    """

    class Meta:
        name = "ComObjectRef_t"

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
    function_text: None | str = field(
        default=None,
        metadata={
            "name": "FunctionText",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    visible_description: None | str = field(
        default=None,
        metadata={
            "name": "VisibleDescription",
            "type": "Attribute",
        },
    )
    priority: None | ComObjectPriority = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Attribute",
        },
    )
    object_size: None | ComObjectSize = field(
        default=None,
        metadata={
            "name": "ObjectSize",
            "type": "Attribute",
        },
    )
    read_flag: None | Enable = field(
        default=None,
        metadata={
            "name": "ReadFlag",
            "type": "Attribute",
        },
    )
    write_flag: None | Enable = field(
        default=None,
        metadata={
            "name": "WriteFlag",
            "type": "Attribute",
        },
    )
    communication_flag: None | Enable = field(
        default=None,
        metadata={
            "name": "CommunicationFlag",
            "type": "Attribute",
        },
    )
    transmit_flag: None | Enable = field(
        default=None,
        metadata={
            "name": "TransmitFlag",
            "type": "Attribute",
        },
    )
    update_flag: None | Enable = field(
        default=None,
        metadata={
            "name": "UpdateFlag",
            "type": "Attribute",
        },
    )
    read_on_init_flag: None | Enable = field(
        default=None,
        metadata={
            "name": "ReadOnInitFlag",
            "type": "Attribute",
        },
    )
    datapoint_type: list[str] = field(
        default_factory=list,
        metadata={
            "name": "DatapointType",
            "type": "Attribute",
            "tokens": True,
        },
    )
