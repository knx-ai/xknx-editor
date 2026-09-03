from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.application_program_channel_t import (
    ApplicationProgramChannel,
)
from xknxmono.models.files.v13.channel_independent_block_t import (
    ChannelIndependentBlock,
)
from xknxmono.models.files.v13.dependent_channel_choose_t import DependentChannelChoose

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramDynamic:
    class Meta:
        name = "ApplicationProgramDynamic_t"

    choice: list[
        ChannelIndependentBlock | ApplicationProgramChannel | DependentChannelChoose
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ChannelIndependentBlock",
                    "type": ChannelIndependentBlock,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "choose",
                    "type": DependentChannelChoose,
                    "namespace": "http://knx.org/xml/project/13",
                },
            ),
        },
    )
