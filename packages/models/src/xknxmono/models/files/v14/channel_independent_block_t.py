from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.application_program_channel_t import (
    ChannelChoose,
    ComObjectParameterBlock,
)
from xknxmono.models.files.v14.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v14.com_object_ref_ref_t import ComObjectRefRef

__NAMESPACE__ = "http://knx.org/xml/project/14"


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
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
            ),
        },
    )
