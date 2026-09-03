from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.module_def_t_arguments_argument import (
    ModuleDefArgumentsArgument,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ModuleDefArguments:
    class Meta:
        global_type = False

    argument: list[ModuleDefArgumentsArgument] = field(
        default_factory=list,
        metadata={
            "name": "Argument",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
