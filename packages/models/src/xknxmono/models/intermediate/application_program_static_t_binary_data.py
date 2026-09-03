from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.binary_data_t import BinaryData


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticBinaryData:
    class Meta:
        global_type = False

    binary_data: list[BinaryData] = field(
        default_factory=list,
        metadata={
            "name": "BinaryData",
            "type": "Element",
        },
    )
