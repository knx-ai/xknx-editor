from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_t import ApplicationProgram


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerApplicationPrograms:
    class Meta:
        global_type = False

    application_program: list[ApplicationProgram] = field(
        default_factory=list,
        metadata={
            "name": "ApplicationProgram",
            "type": "Element",
            "min_occurs": 1,
        },
    )
