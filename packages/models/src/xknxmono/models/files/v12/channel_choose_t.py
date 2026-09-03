from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v12.com_object_parameter_choose_t import (
    ComObjectParameterBlock,
)
from xknxmono.models.files.v12.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v12.rename_t import Rename
from xknxmono.models.files.v12.when_t import When

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ChannelChoose:
    """
    :ivar when: registration-relevant list
    :ivar param_ref_id: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "ChannelChoose_t"

    when: list[ChannelChooseWhen] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
    param_ref_id: str = field(
        metadata={
            "name": "ParamRefId",
            "type": "Attribute",
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
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
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/12",
                },
                {
                    "name": "Rename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/12",
                },
            ),
        },
    )
