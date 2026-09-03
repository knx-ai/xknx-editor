from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.parameter_ref_t import ParameterRef

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParameterRefs:
    """
    :ivar parameter_ref: registration-relevant list This is a list to ensure deterministic
        behaviour in case of multiple active parameter refs
    """

    class Meta:
        global_type = False

    parameter_ref: list[ParameterRef] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
