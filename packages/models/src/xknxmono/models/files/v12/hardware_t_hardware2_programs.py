from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.hardware2_program_t import Hardware2Program

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class HardwareHardware2Programs:
    class Meta:
        global_type = False

    hardware2_program: list[Hardware2Program] = field(
        default_factory=list,
        metadata={
            "name": "Hardware2Program",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
