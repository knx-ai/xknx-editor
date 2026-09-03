from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.parameter_calculation_t import ParameterCalculation


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParameterCalculations:
    """
    :ivar parameter_calculation: registration-relevant set
    """

    class Meta:
        global_type = False

    parameter_calculation: list[ParameterCalculation] = field(
        default_factory=list,
        metadata={
            "name": "ParameterCalculation",
            "type": "Element",
            "min_occurs": 1,
        },
    )
