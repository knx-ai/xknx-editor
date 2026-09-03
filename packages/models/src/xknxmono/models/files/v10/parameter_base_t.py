from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.access_t import Access

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ParameterBase:
    """
    :ivar id: registration-relevant
    :ivar name:
    :ivar parameter_type: registration-relevant
    :ivar text:
    :ivar access:
    :ivar value: registration-relevant
    """

    class Meta:
        name = "ParameterBase_t"

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
            "max_length": 50,
        }
    )
    parameter_type: str = field(
        metadata={
            "name": "ParameterType",
            "type": "Attribute",
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    access: Access = field(
        default=Access.READ_WRITE,
        metadata={
            "name": "Access",
            "type": "Attribute",
        },
    )
    value: str = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
