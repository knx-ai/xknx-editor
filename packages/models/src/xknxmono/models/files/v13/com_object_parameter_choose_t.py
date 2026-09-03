from __future__ import annotations

from dataclasses import dataclass, field
from typing import ForwardRef

from xknxmono.models.files.v13.access_t import Access
from xknxmono.models.files.v13.assign_t import Assign
from xknxmono.models.files.v13.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v13.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v13.parameter_ref_ref_t import ParameterRefRef
from xknxmono.models.files.v13.parameter_separator_t import ParameterSeparator
from xknxmono.models.files.v13.rename_t import Rename
from xknxmono.models.files.v13.when_t import When

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ComObjectParameterChoose:
    """
    :ivar when: registration-relevant list
    :ivar param_ref_id: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "ComObjectParameterChoose_t"

    when: list[ComObjectParameterChooseWhen] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
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
    :ivar text_parameter_ref_id:
    """

    class Meta:
        name = "ComObjectParameterBlock_t"

    choice: list[
        ComObjectParameterBlock
        | ParameterSeparator
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
                    "name": "ParameterBlock",
                    "type": ForwardRef("ComObjectParameterBlock"),
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "ParameterSeparator",
                    "type": ParameterSeparator,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "ParameterRefRef",
                    "type": ParameterRefRef,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "choose",
                    "type": ComObjectParameterChoose,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Assign",
                    "type": Assign,
                    "namespace": "http://knx.org/xml/project/13",
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
    text_parameter_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "TextParameterRefId",
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ComObjectParameterChooseWhen(When):
    class Meta:
        global_type = False

    choice: list[
        ComObjectParameterBlock
        | ParameterSeparator
        | ParameterRefRef
        | ComObjectParameterChoose
        | BinaryDataRef
        | ComObjectRefRef
        | Assign
        | Rename
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterBlock",
                    "type": ComObjectParameterBlock,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "ParameterSeparator",
                    "type": ParameterSeparator,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "ParameterRefRef",
                    "type": ParameterRefRef,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "choose",
                    "type": ComObjectParameterChoose,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Assign",
                    "type": Assign,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Rename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/13",
                },
            ),
        },
    )
