from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.parameter_base_t import ParameterBase

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class UnionParameter(ParameterBase):
    """
    :ivar offset: registration-relevant
    :ivar bit_offset: registration-relevant
    :ivar default_union_parameter: registration-relevant
    """

    class Meta:
        name = "UnionParameter_t"

    offset: int = field(
        metadata={
            "name": "Offset",
            "type": "Attribute",
            "max_inclusive": 1048575,
        }
    )
    bit_offset: int = field(
        metadata={
            "name": "BitOffset",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 7,
        }
    )
    default_union_parameter: bool = field(
        default=False,
        metadata={
            "name": "DefaultUnionParameter",
            "type": "Attribute",
        },
    )
