from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.parameter_type_t import ParameterType

__NAMESPACE__ = "http://knx.org/xml/project/11"


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
            "namespace": "http://knx.org/xml/project/11",
            "min_occurs": 1,
        },
    )
