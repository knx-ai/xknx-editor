from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.channel_choose_t import (
    ApplicationProgramChannel,
    ComObjectParameterBlock,
    Repeat,
)
from xknxmono.models.files.v20.channel_independent_block_t import (
    ChannelIndependentBlock,
)
from xknxmono.models.files.v20.dependent_channel_choose_t import DependentChannelChoose
from xknxmono.models.files.v20.module_t import Module

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "choose",
                    "type": DependentChannelChoose,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "Module",
                    "type": Module,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "Repeat",
                    "type": Repeat,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "ParameterBlock",
                    "type": ComObjectParameterBlock,
                    "namespace": "http://knx.org/xml/project/20",
                },
            ),
        },
    )
