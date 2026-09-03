from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat:
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
    coefficient: None | float = field(
        default=None,
        metadata={
            "name": "Coefficient",
            "type": "Attribute",
        },
    )
    min_value: None | float = field(
        default=None,
        metadata={
            "name": "MinValue",
            "type": "Attribute",
        },
    )
    max_value: None | float = field(
        default=None,
        metadata={
            "name": "MaxValue",
            "type": "Attribute",
        },
    )
    offset: None | float = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Attribute",
        },
    )
