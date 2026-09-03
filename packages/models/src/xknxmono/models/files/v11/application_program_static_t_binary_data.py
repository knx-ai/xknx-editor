from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.binary_data_t import BinaryData

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticBinaryData:
    class Meta:
        global_type = False

    binary_data: list[BinaryData] = field(
        default_factory=list,
        metadata={
            "name": "BinaryData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
            "min_occurs": 1,
        },
    )
