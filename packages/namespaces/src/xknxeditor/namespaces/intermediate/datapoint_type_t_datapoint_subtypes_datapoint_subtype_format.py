from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
)
from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
)


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormat:
    class Meta:
        global_type = False

    choice: list[
        DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatString
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved
        | DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Bit",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit,
                },
                {
                    "name": "UnsignedInteger",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
                },
                {
                    "name": "SignedInteger",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
                },
                {
                    "name": "String",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
                },
                {
                    "name": "Float",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
                },
                {
                    "name": "Enumeration",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
                },
                {
                    "name": "Reserved",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
                },
                {
                    "name": "RefType",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
                },
            ),
        },
    )
