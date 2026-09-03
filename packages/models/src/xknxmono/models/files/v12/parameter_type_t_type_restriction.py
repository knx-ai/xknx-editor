from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.parameter_type_t_type_restriction_base import (
    ParameterTypeTypeRestrictionBase,
)
from xknxmono.models.files.v12.parameter_type_t_type_restriction_enumeration import (
    ParameterTypeTypeRestrictionEnumeration,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeRestriction:
    """
    :ivar enumeration: registration-relevant set
    :ivar base: registration-relevant
    :ivar size_in_bit: registration-relevant
    """

    class Meta:
        global_type = False

    enumeration: list[ParameterTypeTypeRestrictionEnumeration] = field(
        default_factory=list,
        metadata={
            "name": "Enumeration",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    base: ParameterTypeTypeRestrictionBase = field(
        metadata={
            "name": "Base",
            "type": "Attribute",
        }
    )
    size_in_bit: int = field(
        metadata={
            "name": "SizeInBit",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 1048575,
        }
    )
