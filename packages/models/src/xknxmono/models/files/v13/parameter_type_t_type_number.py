from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.parameter_type_t_type_number_type import (
    ParameterTypeTypeNumberType,
)
from xknxmono.models.files.v13.parameter_type_t_type_number_uihint import (
    ParameterTypeTypeNumberUihint,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeNumber:
    """
    :ivar size_in_bit: registration-relevant
    :ivar type_value: registration-relevant
    :ivar min_inclusive: registration-relevant
    :ivar max_inclusive: registration-relevant
    :ivar uihint:
    """

    class Meta:
        global_type = False

    size_in_bit: int = field(
        metadata={
            "name": "SizeInBit",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 32,
        }
    )
    type_value: ParameterTypeTypeNumberType = field(
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    min_inclusive: int = field(
        metadata={
            "name": "minInclusive",
            "type": "Attribute",
        }
    )
    max_inclusive: int = field(
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
        }
    )
    uihint: None | ParameterTypeTypeNumberUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
            "type": "Attribute",
        },
    )
