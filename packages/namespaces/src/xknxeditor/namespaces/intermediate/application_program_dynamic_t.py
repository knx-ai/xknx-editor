from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.intermediate.application_program_channel_t import (
    ApplicationProgramChannel,
    Repeat,
)
from xknxeditor.namespaces.intermediate.channel_independent_block_t import (
    ChannelIndependentBlock,
)
from xknxeditor.namespaces.intermediate.dependent_channel_choose_t import (
    DependentChannelChoose,
)
from xknxeditor.namespaces.intermediate.module_t import Module


@dataclass(slots=True, kw_only=True)
class ApplicationProgramDynamic:
    class Meta:
        name = "ApplicationProgramDynamic_t"

    choice: list[
        ChannelIndependentBlock
        | ApplicationProgramChannel
        | DependentChannelChoose
        | Module
        | Repeat
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
            ),
        },
    )
