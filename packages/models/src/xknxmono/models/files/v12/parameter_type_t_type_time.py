from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.parameter_type_t_type_time_uihint import (
    ParameterTypeTypeTimeUihint,
)
from xknxmono.models.files.v12.parameter_type_t_type_time_unit import (
    ParameterTypeTypeTimeUnit,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeTime:
    """
    :ivar size_in_bit: registration-relevant
    :ivar unit: registration-relevant
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
            "min_inclusive": 8,
            "max_inclusive": 64,
        }
    )
    unit: ParameterTypeTypeTimeUnit = field(
        metadata={
            "name": "Unit",
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
    uihint: None | ParameterTypeTypeTimeUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
            "type": "Attribute",
        },
    )
