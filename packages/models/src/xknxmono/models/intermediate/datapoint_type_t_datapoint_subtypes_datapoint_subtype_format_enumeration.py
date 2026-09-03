from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration_enum_value import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue,
)


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration:
    class Meta:
        global_type = False

    enum_value: list[
        DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue
    ] = field(
        default_factory=list,
        metadata={
            "name": "EnumValue",
            "type": "Element",
        },
    )
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
