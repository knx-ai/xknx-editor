from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
)
from xknxmono.models.files.v21.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


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
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "UnsignedInteger",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "SignedInteger",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "String",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Float",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Enumeration",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Reserved",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "RefType",
                    "type": DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
                    "namespace": "http://knx.org/xml/project/21",
                },
            ),
        },
    )
