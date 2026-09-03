from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_channel_t import (
    ApplicationProgramChannel,
    ComObjectParameterBlock,
    Repeat,
)
from xknxmono.models.intermediate.channel_independent_block_t import (
    ChannelIndependentBlock,
)
from xknxmono.models.intermediate.dependent_channel_choose_t import (
    DependentChannelChoose,
)
from xknxmono.models.intermediate.module_t import Module


@dataclass(slots=True, kw_only=True)
class ModuleDefDynamic:
    class Meta:
        name = "ModuleDefDynamic_t"

    choice: list[
        ChannelIndependentBlock
        | ApplicationProgramChannel
        | DependentChannelChoose
        | Module
        | Repeat
        | ComObjectParameterBlock
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ChannelIndependentBlock",
                    "type": ChannelIndependentBlock,
                },
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                },
                {
                    "name": "choose",
                    "type": DependentChannelChoose,
                },
                {
                    "name": "Module",
                    "type": Module,
                },
                {
                    "name": "Repeat",
                    "type": Repeat,
                },
                {
                    "name": "ParameterBlock",
                    "type": ComObjectParameterBlock,
                },
            ),
        },
    )
