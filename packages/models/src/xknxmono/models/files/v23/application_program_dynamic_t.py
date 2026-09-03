from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.channel_choose_t import (
    ApplicationProgramChannel,
    Repeat,
)
from xknxmono.models.files.v23.channel_independent_block_t import (
    ChannelIndependentBlock,
)
from xknxmono.models.files.v23.dependent_channel_choose_t import DependentChannelChoose
from xknxmono.models.files.v23.module_t import Module

__NAMESPACE__ = "http://knx.org/xml/project/23"


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
                    "namespace": "http://knx.org/xml/project/23",
                },
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                    "namespace": "http://knx.org/xml/project/23",
                },
                {
                    "name": "choose",
                    "type": DependentChannelChoose,
                    "namespace": "http://knx.org/xml/project/23",
                },
                {
                    "name": "Module",
                    "type": Module,
                    "namespace": "http://knx.org/xml/project/23",
                },
                {
                    "name": "Repeat",
                    "type": Repeat,
                    "namespace": "http://knx.org/xml/project/23",
                },
            ),
        },
    )
