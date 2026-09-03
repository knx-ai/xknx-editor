from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v10.com_object_parameter_block_t import (
    ComObjectParameterBlock,
)
from xknxmono.models.files.v10.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v10.rename_t import Rename
from xknxmono.models.files.v10.when_t import When

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ChannelChoose:
    """
    :ivar when: registration-relevant list
    :ivar param_ref_id: registration-relevant
    """

    class Meta:
        name = "ChannelChoose_t"

    when: list[ChannelChooseWhen] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
    param_ref_id: str = field(
        metadata={
            "name": "ParamRefId",
            "type": "Attribute",
        }
    )


@dataclass(slots=True, kw_only=True)
class ChannelChooseWhen(When):
    class Meta:
        global_type = False

    choice: list[
        ComObjectParameterBlock
        | ComObjectRefRef
        | BinaryDataRef
        | ChannelChoose
        | Rename
    ] = field(
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
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "ParameterBlockRename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/10",
                },
            ),
        },
    )
