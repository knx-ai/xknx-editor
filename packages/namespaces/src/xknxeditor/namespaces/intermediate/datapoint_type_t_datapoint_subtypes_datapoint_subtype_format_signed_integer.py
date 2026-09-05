from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger:
    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    width: int = field(
        metadata={
            "name": "Width",
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
    unit: None | str = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Attribute",
        },
    )
    min_inclusive: None | int = field(
        default=None,
        metadata={
            "name": "MinInclusive",
            "type": "Attribute",
        },
    )
    max_inclusive: None | int = field(
        default=None,
        metadata={
            "name": "MaxInclusive",
            "type": "Attribute",
        },
    )
    coefficient: None | float = field(
        default=None,
        metadata={
            "name": "Coefficient",
            "type": "Attribute",
        },
    )
    offset: None | int = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Attribute",
        },
    )
