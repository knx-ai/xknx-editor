from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.module_instance_t_arguments_argument import (
    ModuleInstanceArgumentsArgument,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ModuleInstanceArguments:
    class Meta:
        global_type = False

    argument: list[ModuleInstanceArgumentsArgument] = field(
        default_factory=list,
        metadata={
            "name": "Argument",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
