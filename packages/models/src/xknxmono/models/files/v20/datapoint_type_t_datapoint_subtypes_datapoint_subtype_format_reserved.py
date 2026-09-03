from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved:
    class Meta:
        global_type = False

    width: int = field(
        metadata={
            "name": "Width",
            "type": "Attribute",
        }
    )
