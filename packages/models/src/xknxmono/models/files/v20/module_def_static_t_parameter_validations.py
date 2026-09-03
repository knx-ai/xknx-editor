from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.parameter_validation_t import ParameterValidation

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParameterValidations:
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
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
