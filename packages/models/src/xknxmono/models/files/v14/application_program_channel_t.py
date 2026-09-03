from __future__ import annotations

from dataclasses import dataclass, field
from typing import ForwardRef

from xknxmono.models.files.v14.access_t import Access
from xknxmono.models.files.v14.assign_t import Assign
from xknxmono.models.files.v14.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v14.button_t import Button
from xknxmono.models.files.v14.com_object_parameter_block_t_columns import (
    ComObjectParameterBlockColumns,
)
from xknxmono.models.files.v14.com_object_parameter_block_t_rows import (
    ComObjectParameterBlockRows,
)
from xknxmono.models.files.v14.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v14.parameter_block_layout_t import ParameterBlockLayout
from xknxmono.models.files.v14.parameter_ref_ref_t import ParameterRefRef
from xknxmono.models.files.v14.parameter_separator_t import ParameterSeparator
from xknxmono.models.files.v14.rename_t import Rename
from xknxmono.models.files.v14.when_t import When

__NAMESPACE__ = "http://knx.org/xml/project/14"


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
            "namespace": "http://knx.org/xml/project/14",
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
            "namespace": "http://knx.org/xml/project/14",
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
class ApplicationProgramChannel:
    """
    :ivar choice:
    :ivar name:
    :ivar text:
    :ivar number: registration-relevant
    :ivar id: registration-relevant
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    :ivar icon:
    :ivar help_context:
    """

    class Meta:
        name = "ApplicationProgramChannel_t"

    choice: list[
        ComObjectParameterBlock | ComObjectRefRef | BinaryDataRef | ChannelChoose
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterBlock",
                    "type": ForwardRef("ComObjectParameterBlock"),
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "choose",
                    "type": ForwardRef("ChannelChoose"),
                    "namespace": "http://knx.org/xml/project/14",
                },
            ),
        },
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    number: str = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    text_parameter_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "TextParameterRefId",
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
    icon: None | str = field(
        default=None,
        metadata={
            "name": "Icon",
            "type": "Attribute",
        },
    )
    help_context: None | str = field(
        default=None,
        metadata={
            "name": "HelpContext",
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ComObjectParameterBlock:
    """
    :ivar rows:
    :ivar columns:
    :ivar choice:
    :ivar id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar access:
    :ivar help_topic:
    :ivar internal_description:
    :ivar param_ref_id: registration-relevant
    :ivar text_parameter_ref_id:
    :ivar inline:
    :ivar layout:
    :ivar cell:
    :ivar icon:
    :ivar help_context:
    :ivar show_in_com_object_tree:
    """

    class Meta:
        name = "ComObjectParameterBlock_t"

    rows: None | ComObjectParameterBlockRows = field(
        default=None,
        metadata={
            "name": "Rows",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
        },
    )
    columns: None | ComObjectParameterBlockColumns = field(
        default=None,
        metadata={
            "name": "Columns",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
        },
    )
    choice: list[
        ComObjectParameterBlock
        | ParameterSeparator
        | ParameterRefRef
        | Button
        | ComObjectParameterChoose
        | BinaryDataRef
        | ComObjectRefRef
        | Assign
        | ApplicationProgramChannel
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterBlock",
                    "type": ForwardRef("ComObjectParameterBlock"),
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ParameterSeparator",
                    "type": ParameterSeparator,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ParameterRefRef",
                    "type": ParameterRefRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "Button",
                    "type": Button,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "choose",
                    "type": ComObjectParameterChoose,
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
                {
                    "name": "Assign",
                    "type": Assign,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                    "namespace": "http://knx.org/xml/project/14",
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
    inline: bool = field(
        default=False,
        metadata={
            "name": "Inline",
            "type": "Attribute",
        },
    )
    layout: ParameterBlockLayout = field(
        default=ParameterBlockLayout.LIST,
        metadata={
            "name": "Layout",
            "type": "Attribute",
        },
    )
    cell: None | str = field(
        default=None,
        metadata={
            "name": "Cell",
            "type": "Attribute",
            "pattern": r"\d+,\d+",
        },
    )
    icon: None | str = field(
        default=None,
        metadata={
            "name": "Icon",
            "type": "Attribute",
        },
    )
    help_context: None | str = field(
        default=None,
        metadata={
            "name": "HelpContext",
            "type": "Attribute",
        },
    )
    show_in_com_object_tree: bool = field(
        default=False,
        metadata={
            "name": "ShowInComObjectTree",
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
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "choose",
                    "type": ChannelChoose,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "Rename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/14",
                },
            ),
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
        | Button
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
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ParameterSeparator",
                    "type": ParameterSeparator,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "ParameterRefRef",
                    "type": ParameterRefRef,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "Button",
                    "type": Button,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "choose",
                    "type": ComObjectParameterChoose,
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
                {
                    "name": "Assign",
                    "type": Assign,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "Rename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/14",
                },
            ),
        },
    )
