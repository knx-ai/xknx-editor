from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v12.channel_choose_t import ChannelChoose
from xknxmono.models.files.v12.com_object_parameter_choose_t import (
    ComObjectParameterBlock,
)
from xknxmono.models.files.v12.com_object_ref_ref_t import ComObjectRefRef

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramChannel:
    """
    :ivar choice:
    :ivar name:
    :ivar text:
    :ivar number: registration-relevant
    :ivar id: registration-relevant
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    """

    class Meta:
        name = "ApplicationProgramChannel_t"

    choice: list[
        ComObjectParameterBlock | ComObjectRefRef | BinaryDataRef | ChannelChoose
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterBlock",
                    "type": ComObjectParameterBlock,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/12",
                },
            ),
        },
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    number: str = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
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
