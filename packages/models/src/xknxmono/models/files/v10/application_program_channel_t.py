from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v10.channel_choose_t import ChannelChoose
from xknxmono.models.files.v10.com_object_parameter_block_t import (
    ComObjectParameterBlock,
)
from xknxmono.models.files.v10.com_object_ref_ref_t import ComObjectRefRef

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramChannel:
    """
    :ivar choice:
    :ivar name:
    :ivar text:
    :ivar number: registration-relevant
    :ivar id: registration-relevant
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
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/10",
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
