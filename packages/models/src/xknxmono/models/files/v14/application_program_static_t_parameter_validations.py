from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.parameter_validation_t import ParameterValidation

__NAMESPACE__ = "http://knx.org/xml/project/14"


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
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
