from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.parameter_type_t_type_color import ParameterTypeTypeColor
from xknxmono.models.files.v21.parameter_type_t_type_date import ParameterTypeTypeDate
from xknxmono.models.files.v21.parameter_type_t_type_float import ParameterTypeTypeFloat
from xknxmono.models.files.v21.parameter_type_t_type_ipaddress import (
    ParameterTypeTypeIpaddress,
)
from xknxmono.models.files.v21.parameter_type_t_type_number import (
    ParameterTypeTypeNumber,
)
from xknxmono.models.files.v21.parameter_type_t_type_picture import (
    ParameterTypeTypePicture,
)
from xknxmono.models.files.v21.parameter_type_t_type_raw_data import (
    ParameterTypeTypeRawData,
)
from xknxmono.models.files.v21.parameter_type_t_type_restriction import (
    ParameterTypeTypeRestriction,
)
from xknxmono.models.files.v21.parameter_type_t_type_text import ParameterTypeTypeText
from xknxmono.models.files.v21.parameter_type_t_type_time import ParameterTypeTypeTime

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ParameterType:
    """
    :ivar choice:
    :ivar id: registration-relevant
    :ivar name: registration-relevant
    :ivar internal_description:
    :ivar plugin:
    :ivar validation_error_ref:
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
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeFloat",
                    "type": ParameterTypeTypeFloat,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeRestriction",
                    "type": ParameterTypeTypeRestriction,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeText",
                    "type": ParameterTypeTypeText,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeTime",
                    "type": ParameterTypeTypeTime,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeDate",
                    "type": ParameterTypeTypeDate,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeIPAddress",
                    "type": ParameterTypeTypeIpaddress,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypePicture",
                    "type": ParameterTypeTypePicture,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeColor",
                    "type": ParameterTypeTypeColor,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeRawData",
                    "type": ParameterTypeTypeRawData,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "TypeNone",
                    "type": object,
                    "namespace": "http://knx.org/xml/project/21",
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
