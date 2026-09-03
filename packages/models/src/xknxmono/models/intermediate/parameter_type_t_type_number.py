from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.parameter_type_t_type_number_type import (
    ParameterTypeTypeNumberType,
)
from xknxmono.models.intermediate.parameter_type_t_type_number_uihint import (
    ParameterTypeTypeNumberUihint,
)


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeNumber:
    """
    :ivar size_in_bit: registration-relevant
    :ivar type_value: registration-relevant
    :ivar min_inclusive: registration-relevant
    :ivar max_inclusive: registration-relevant
    :ivar increment: registration-relevant
    :ivar uihint:
    :ivar display_offset:
    :ivar display_factor:
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
    increment: int = field(
        default=1,
        metadata={
            "name": "Increment",
            "type": "Attribute",
        },
    )
    uihint: None | ParameterTypeTypeNumberUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
            "type": "Attribute",
        },
    )
    display_offset: None | float = field(
        default=None,
        metadata={
            "name": "DisplayOffset",
            "type": "Attribute",
        },
    )
    display_factor: None | float = field(
        default=None,
        metadata={
            "name": "DisplayFactor",
            "type": "Attribute",
        },
    )
