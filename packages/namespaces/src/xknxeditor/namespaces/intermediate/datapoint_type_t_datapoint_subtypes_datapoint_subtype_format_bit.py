from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit:
    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        },
    )
    set: str = field(
        metadata={
            "name": "Set",
            "type": "Attribute",
        }
    )
    cleared: str = field(
        metadata={
            "name": "Cleared",
            "type": "Attribute",
        }
    )
