from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v10.channel_choose_t import ChannelChoose
from xknxmono.models.files.v10.com_object_parameter_block_t import (
    ComObjectParameterBlock,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ChannelIndependentBlock:
    class Meta:
        name = "ChannelIndependentBlock_t"

    choice: list[ComObjectParameterBlock | ChannelChoose | BinaryDataRef] = field(
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
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/10",
                },
            ),
        },
    )
