from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_def_static_t_parameters_parameter import (
    ModuleDefStaticParametersParameter,
)
from xknxmono.models.intermediate.module_def_static_t_parameters_union import (
    ModuleDefStaticParametersUnion,
)


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParameters:
    class Meta:
        global_type = False

    choice: list[
        ModuleDefStaticParametersParameter | ModuleDefStaticParametersUnion
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Parameter",
                    "type": ModuleDefStaticParametersParameter,
                },
                {
                    "name": "Union",
                    "type": ModuleDefStaticParametersUnion,
                },
            ),
        },
    )
