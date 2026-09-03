from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.access_t import Access
from xknxmono.models.files.v11.assign_t import Assign
from xknxmono.models.files.v11.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v11.com_object_parameter_choose_t import (
    ComObjectParameterChoose,
)
from xknxmono.models.files.v11.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v11.parameter_ref_ref_t import ParameterRefRef
from xknxmono.models.files.v11.parameter_separator_t import ParameterSeparator

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ComObjectParameterBlock:
    """
    :ivar choice:
    :ivar id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar access:
    :ivar help_topic:
    :ivar internal_description:
    :ivar param_ref_id: registration-relevant
    """

    class Meta:
        name = "ComObjectParameterBlock_t"

    choice: list[
        ParameterSeparator
        | ParameterRefRef
        | ComObjectParameterChoose
        | BinaryDataRef
        | ComObjectRefRef
        | Assign
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterSeparator",
                    "type": ParameterSeparator,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "ParameterRefRef",
                    "type": ParameterRefRef,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "choose",
                    "type": ComObjectParameterChoose,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "Assign",
                    "type": Assign,
                    "namespace": "http://knx.org/xml/project/11",
                },
            ),
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    access: Access = field(
        default=Access.READ_WRITE,
        metadata={
            "name": "Access",
            "type": "Attribute",
        },
    )
    help_topic: None | int = field(
        default=None,
        metadata={
            "name": "HelpTopic",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    param_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "ParamRefId",
            "type": "Attribute",
        },
    )
