from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.parameter_calculation_t import ParameterCalculation

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParameterCalculations:
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
            "namespace": "http://knx.org/xml/project/11",
            "min_occurs": 1,
        },
    )
