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
class ChannelIndependentBlock:
    class Meta:
        name = "ChannelIndependentBlock_t"

    choice: list[
        ComObjectParameterBlock | ChannelChoose | BinaryDataRef | ComObjectRefRef
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
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/12",
                },
            ),
        },
    )
