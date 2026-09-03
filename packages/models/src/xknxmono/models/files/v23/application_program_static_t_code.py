from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.application_program_static_t_code_absolute_segment import (
    ApplicationProgramStaticCodeAbsoluteSegment,
)
from xknxmono.models.files.v23.application_program_static_t_code_relative_segment import (
    ApplicationProgramStaticCodeRelativeSegment,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticCode:
    """
    :ivar absolute_segment: registration-relevant set
    :ivar relative_segment: registration-relevant set
    """

    class Meta:
        global_type = False

    absolute_segment: list[ApplicationProgramStaticCodeAbsoluteSegment] = field(
        default_factory=list,
        metadata={
            "name": "AbsoluteSegment",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    relative_segment: list[ApplicationProgramStaticCodeRelativeSegment] = field(
        default_factory=list,
        metadata={
            "name": "RelativeSegment",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
