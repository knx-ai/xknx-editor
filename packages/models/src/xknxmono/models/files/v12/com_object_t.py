from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.com_object_priority_t import ComObjectPriority
from xknxmono.models.files.v12.com_object_size_t import ComObjectSize
from xknxmono.models.files.v12.enable_t import Enable

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ComObject:
    """
    :ivar id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar number: registration-relevant
    :ivar function_text:
    :ivar priority:
    :ivar object_size: registration-relevant
    :ivar read_flag:
    :ivar write_flag:
    :ivar communication_flag:
    :ivar transmit_flag:
    :ivar update_flag:
    :ivar read_on_init_flag:
    :ivar datapoint_type:
    :ivar internal_description:
    """

    class Meta:
        name = "ComObject_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    function_text: str = field(
        metadata={
            "name": "FunctionText",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    priority: ComObjectPriority = field(
        default=ComObjectPriority.LOW,
        metadata={
            "name": "Priority",
            "type": "Attribute",
        },
    )
    object_size: ComObjectSize = field(
        metadata={
            "name": "ObjectSize",
            "type": "Attribute",
        }
    )
    read_flag: Enable = field(
        metadata={
            "name": "ReadFlag",
            "type": "Attribute",
        }
    )
    write_flag: Enable = field(
        metadata={
            "name": "WriteFlag",
            "type": "Attribute",
        }
    )
    communication_flag: Enable = field(
        metadata={
            "name": "CommunicationFlag",
            "type": "Attribute",
        }
    )
    transmit_flag: Enable = field(
        metadata={
            "name": "TransmitFlag",
            "type": "Attribute",
        }
    )
    update_flag: Enable = field(
        metadata={
            "name": "UpdateFlag",
            "type": "Attribute",
        }
    )
    read_on_init_flag: Enable = field(
        metadata={
            "name": "ReadOnInitFlag",
            "type": "Attribute",
        }
    )
    datapoint_type: list[str] = field(
        default_factory=list,
        metadata={
            "name": "DatapointType",
            "type": "Attribute",
            "tokens": True,
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
