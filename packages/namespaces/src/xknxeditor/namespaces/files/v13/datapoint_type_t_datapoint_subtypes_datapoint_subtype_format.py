from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
)
from xknxeditor.namespaces.files.v13.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


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
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "UnsignedInteger",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "SignedInteger",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "String",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Float",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Enumeration",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "Reserved",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
                    "namespace": "http://knx.org/xml/project/13",
                },
                {
                    "name": "RefType",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
                    "namespace": "http://knx.org/xml/project/13",
                },
            ),
        },
    )
