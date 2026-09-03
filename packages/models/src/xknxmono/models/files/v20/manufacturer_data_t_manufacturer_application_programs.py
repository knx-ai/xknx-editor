from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.application_program_t import ApplicationProgram

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerApplicationPrograms:
    class Meta:
        global_type = False

    application_program: list[ApplicationProgram] = field(
        default_factory=list,
        metadata={
            "name": "ApplicationProgram",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
