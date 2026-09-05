from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType:
    class Meta:
        global_type = False

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
