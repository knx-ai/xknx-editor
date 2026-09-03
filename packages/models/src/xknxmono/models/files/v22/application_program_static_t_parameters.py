from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.application_program_static_t_parameters_parameter import (
    ApplicationProgramStaticParametersParameter,
)
from xknxmono.models.files.v22.application_program_static_t_parameters_union import (
    ApplicationProgramStaticParametersUnion,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


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
                    "namespace": "http://knx.org/xml/project/22",
                },
                {
                    "name": "Union",
                    "type": ApplicationProgramStaticParametersUnion,
                    "namespace": "http://knx.org/xml/project/22",
                },
            ),
        },
    )
