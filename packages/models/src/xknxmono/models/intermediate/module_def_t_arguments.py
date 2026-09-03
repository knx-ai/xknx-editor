from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_def_t_arguments_argument import (
    ModuleDefArgumentsArgument,
)


@dataclass(slots=True, kw_only=True)
class ModuleDefArguments:
    class Meta:
        global_type = False

    argument: list[ModuleDefArgumentsArgument] = field(
        default_factory=list,
        metadata={
            "name": "Argument",
            "type": "Element",
            "min_occurs": 1,
        },
    )
