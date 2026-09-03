from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.calculation_parameter_ref_t import (
    CalculationParameterRef,
)


@dataclass(slots=True, kw_only=True)
class ParameterCalculationRparameters:
    """
    :ivar parameter_ref_ref: registration-relevant set
    """

    class Meta:
        global_type = False

    parameter_ref_ref: list[CalculationParameterRef] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRefRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )
