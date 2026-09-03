from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_parameters_parameter import (
    ApplicationProgramStaticParametersParameter,
)
from xknxmono.models.intermediate.application_program_static_t_parameters_union import (
    ApplicationProgramStaticParametersUnion,
)


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParameters:
    class Meta:
        global_type = False

    choice: list[
        ApplicationProgramStaticParametersParameter
        | ApplicationProgramStaticParametersUnion
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Parameter",
                    "type": ApplicationProgramStaticParametersParameter,
                },
                {
                    "name": "Union",
                    "type": ApplicationProgramStaticParametersUnion,
                },
            ),
        },
    )
