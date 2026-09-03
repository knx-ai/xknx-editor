from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.parameter_type_t_type_color import (
    ParameterTypeTypeColor,
)
from xknxmono.models.intermediate.parameter_type_t_type_date import (
    ParameterTypeTypeDate,
)
from xknxmono.models.intermediate.parameter_type_t_type_float import (
    ParameterTypeTypeFloat,
)
from xknxmono.models.intermediate.parameter_type_t_type_ipaddress import (
    ParameterTypeTypeIpaddress,
)
from xknxmono.models.intermediate.parameter_type_t_type_number import (
    ParameterTypeTypeNumber,
)
from xknxmono.models.intermediate.parameter_type_t_type_picture import (
    ParameterTypeTypePicture,
)
from xknxmono.models.intermediate.parameter_type_t_type_raw_data import (
    ParameterTypeTypeRawData,
)
from xknxmono.models.intermediate.parameter_type_t_type_restriction import (
    ParameterTypeTypeRestriction,
)
from xknxmono.models.intermediate.parameter_type_t_type_text import (
    ParameterTypeTypeText,
)
from xknxmono.models.intermediate.parameter_type_t_type_time import (
    ParameterTypeTypeTime,
)
from xknxmono.models.intermediate.text_alignment_t import TextAlignment


@dataclass(slots=True, kw_only=True)
class ParameterType:
    """
    :ivar choice:
    :ivar id: registration-relevant
    :ivar name: registration-relevant
    :ivar internal_description:
    :ivar plugin:
    :ivar validation_error_ref:
    :ivar text_alignment:
    :ivar io_tencoding: registration-relevant
    """

    class Meta:
        name = "ParameterType_t"

    choice: (
        None
        | ParameterTypeTypeNumber
        | ParameterTypeTypeFloat
        | ParameterTypeTypeRestriction
        | ParameterTypeTypeText
        | ParameterTypeTypeTime
        | ParameterTypeTypeDate
        | ParameterTypeTypeIpaddress
        | ParameterTypeTypePicture
        | ParameterTypeTypeColor
        | ParameterTypeTypeRawData
        | object
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "TypeNumber",
                    "type": ParameterTypeTypeNumber,
                },
                {
                    "name": "TypeFloat",
                    "type": ParameterTypeTypeFloat,
                },
                {
                    "name": "TypeRestriction",
                    "type": ParameterTypeTypeRestriction,
                },
                {
                    "name": "TypeText",
                    "type": ParameterTypeTypeText,
                },
                {
                    "name": "TypeTime",
                    "type": ParameterTypeTypeTime,
                },
                {
                    "name": "TypeDate",
                    "type": ParameterTypeTypeDate,
                },
                {
                    "name": "TypeIPAddress",
                    "type": ParameterTypeTypeIpaddress,
                },
                {
                    "name": "TypePicture",
                    "type": ParameterTypeTypePicture,
                },
                {
                    "name": "TypeColor",
                    "type": ParameterTypeTypeColor,
                },
                {
                    "name": "TypeRawData",
                    "type": ParameterTypeTypeRawData,
                },
                {
                    "name": "TypeNone",
                    "type": object,
                },
            ),
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    plugin: None | str = field(
        default=None,
        metadata={
            "name": "Plugin",
            "type": "Attribute",
        },
    )
    validation_error_ref: None | str = field(
        default=None,
        metadata={
            "name": "ValidationErrorRef",
            "type": "Attribute",
        },
    )
    text_alignment: None | TextAlignment = field(
        default=None,
        metadata={
            "name": "TextAlignment",
            "type": "Attribute",
        },
    )
    io_tencoding: None | str = field(
        default=None,
        metadata={
            "name": "IoTEncoding",
            "type": "Attribute",
        },
    )
