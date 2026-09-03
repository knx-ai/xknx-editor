from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_def_dynamic_t import ModuleDefDynamic
from xknxmono.models.intermediate.module_def_static_t import ModuleDefStatic
from xknxmono.models.intermediate.module_def_t_arguments import ModuleDefArguments


@dataclass(slots=True, kw_only=True)
class ModuleDef:
    class Meta:
        name = "ModuleDef_t"

    arguments: None | ModuleDefArguments = field(
        default=None,
        metadata={
            "name": "Arguments",
            "type": "Element",
        },
    )
    static: ModuleDefStatic = field(
        metadata={
            "name": "Static",
            "type": "Element",
        }
    )
    sub_module_defs: None | ModuleDefSubModuleDefs = field(
        default=None,
        metadata={
            "name": "SubModuleDefs",
            "type": "Element",
        },
    )
    dynamic: None | ModuleDefDynamic = field(
        default=None,
        metadata={
            "name": "Dynamic",
            "type": "Element",
        },
    )
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
            "max_length": 255,
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
class ModuleDefSubModuleDefs:
    """
    :ivar module_def: registration-relevant set
    """

    class Meta:
        global_type = False

    module_def: list[ModuleDef] = field(
        default_factory=list,
        metadata={
            "name": "ModuleDef",
            "type": "Element",
            "min_occurs": 1,
        },
    )
