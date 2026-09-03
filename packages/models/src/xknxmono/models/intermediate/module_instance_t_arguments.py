from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_instance_t_arguments_argument import (
    ModuleInstanceArgumentsArgument,
)


@dataclass(slots=True, kw_only=True)
class ModuleInstanceArguments:
    class Meta:
        global_type = False

    argument: list[ModuleInstanceArgumentsArgument] = field(
        default_factory=list,
        metadata={
            "name": "Argument",
            "type": "Element",
            "min_occurs": 1,
        },
    )
