from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.parameter_calculation_t import ParameterCalculation

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
