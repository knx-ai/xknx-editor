from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.parameter_type_t_type_restriction_base import (
    ParameterTypeTypeRestrictionBase,
)
from xknxmono.models.files.v21.parameter_type_t_type_restriction_enumeration import (
    ParameterTypeTypeRestrictionEnumeration,
)
from xknxmono.models.files.v21.parameter_type_t_type_restriction_uihint import (
    ParameterTypeTypeRestrictionUihint,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeRestriction:
    """
    :ivar enumeration: registration-relevant set
    :ivar base: registration-relevant
    :ivar size_in_bit: registration-relevant
    :ivar uihint:
    """

    class Meta:
        global_type = False

    enumeration: list[ParameterTypeTypeRestrictionEnumeration] = field(
        default_factory=list,
        metadata={
            "name": "Enumeration",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
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
    uihint: None | ParameterTypeTypeRestrictionUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
            "type": "Attribute",
        },
    )
