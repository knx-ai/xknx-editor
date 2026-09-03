from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.access_t import Access

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ParameterSeparator:
    """
    :ivar id: registration-relevant
    :ivar text:
    :ivar access:
    """

    class Meta:
        name = "ParameterSeparator_t"

    id: str = field(
        metadata={
            "name": "Id",
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
