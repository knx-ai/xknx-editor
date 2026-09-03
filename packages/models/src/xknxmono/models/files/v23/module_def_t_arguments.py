from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.module_def_t_arguments_argument import (
    ModuleDefArgumentsArgument,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ModuleDefArguments:
    class Meta:
        global_type = False

    argument: list[ModuleDefArgumentsArgument] = field(
        default_factory=list,
        metadata={
            "name": "Argument",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
