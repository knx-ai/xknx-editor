from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.module_def_arg_type_t import ModuleDefArgType
from xknxmono.models.files.v20.module_def_t_arguments_argument_alignment import (
    ModuleDefArgumentsArgumentAlignment,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ModuleDefArgumentsArgument:
    """
    :ivar id:
    :ivar name: registration-relevant
    :ivar type_value: registration-relevant
    :ivar internal_description:
    :ivar allocates: registration-relevant
    :ivar alignment: registration-relevant
    """

    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
            "pattern": r"[A-Za-z_][A-Za-z0-9_]*",
        }
    )
    type_value: ModuleDefArgType = field(
        default=ModuleDefArgType.NUMERIC,
        metadata={
            "name": "Type",
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
    allocates: None | int = field(
        default=None,
        metadata={
            "name": "Allocates",
            "type": "Attribute",
        },
    )
    alignment: ModuleDefArgumentsArgumentAlignment = field(
        default=ModuleDefArgumentsArgumentAlignment.VALUE_1,
        metadata={
            "name": "Alignment",
            "type": "Attribute",
        },
    )
