from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v21.channel_choose_t import (
    ChannelChoose,
    ComObjectParameterBlock,
    Repeat,
)
from xknxmono.models.files.v21.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v21.module_t import Module

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ChannelIndependentBlock:
    class Meta:
        name = "ChannelIndependentBlock_t"

    choice: list[
        ComObjectParameterBlock
        | ChannelChoose
        | BinaryDataRef
        | ComObjectRefRef
        | Module
        | Repeat
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterBlock",
                    "type": ComObjectParameterBlock,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Module",
                    "type": Module,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Repeat",
                    "type": Repeat,
                    "namespace": "http://knx.org/xml/project/21",
                },
            ),
        },
    )
