from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.hardware_t import Hardware


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerHardware:
    class Meta:
        global_type = False

    hardware: list[Hardware] = field(
        default_factory=list,
        metadata={
            "name": "Hardware",
            "type": "Element",
        },
    )
