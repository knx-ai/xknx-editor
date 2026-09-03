from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_channel_t import (
    ChannelChoose,
    ComObjectParameterBlock,
    Repeat,
)
from xknxmono.models.intermediate.binary_data_ref_t import BinaryDataRef
from xknxmono.models.intermediate.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.intermediate.module_t import Module


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
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                },
                {
                    "name": "Module",
                    "type": Module,
                },
                {
                    "name": "Repeat",
                    "type": Repeat,
                },
            ),
        },
    )
