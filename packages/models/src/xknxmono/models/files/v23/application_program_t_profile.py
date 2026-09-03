from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.application_program_t_profile_io_t import (
    ApplicationProgramProfileIo,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramProfile:
    class Meta:
        global_type = False

    io_t: None | ApplicationProgramProfileIo = field(
        default=None,
        metadata={
            "name": "IoT",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
