from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.parameter_type_t_type_float_encoding import (
    ParameterTypeTypeFloatEncoding,
)
from xknxmono.models.files.v12.parameter_type_t_type_float_uihint import (
    ParameterTypeTypeFloatUihint,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeFloat:
    """
    :ivar encoding: registration-relevant
    :ivar min_inclusive: registration-relevant
    :ivar max_inclusive: registration-relevant
    :ivar uihint:
    :ivar display_format:
    """

    class Meta:
        global_type = False

    encoding: ParameterTypeTypeFloatEncoding = field(
        metadata={
            "name": "Encoding",
            "type": "Attribute",
        }
    )
    min_inclusive: float = field(
        metadata={
            "name": "minInclusive",
            "type": "Attribute",
        }
    )
    max_inclusive: float = field(
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
        }
    )
    uihint: None | ParameterTypeTypeFloatUihint = field(
        default=None,
        metadata={
            "name": "UIHint",
            "type": "Attribute",
        },
    )
    display_format: None | str = field(
        default=None,
        metadata={
            "name": "DisplayFormat",
            "type": "Attribute",
            "pattern": r"[#,]*[0,]+(\.0*)?([eE][+-]?0+)?",
        },
    )
