from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.parameter_validation_t import ParameterValidation


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParameterValidations:
    """
    :ivar parameter_validation: registration-relevant set
    """

    class Meta:
        global_type = False

    parameter_validation: list[ParameterValidation] = field(
        default_factory=list,
        metadata={
            "name": "ParameterValidation",
            "type": "Element",
        },
    )
