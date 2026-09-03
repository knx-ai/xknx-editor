from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.parameter_type_t import ParameterType


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParameterTypes:
    """
    :ivar parameter_type: registration-relevant set
    """

    class Meta:
        global_type = False

    parameter_type: list[ParameterType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterType",
            "type": "Element",
            "min_occurs": 1,
        },
    )
