from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.parameter_type_t_type_date_encoding import (
    ParameterTypeTypeDateEncoding,
)


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeDate:
    """
    :ivar encoding: registration-relevant
    :ivar display_the_year: registration-relevant
    """

    class Meta:
        global_type = False

    encoding: ParameterTypeTypeDateEncoding = field(
        metadata={
            "name": "Encoding",
            "type": "Attribute",
        }
    )
    display_the_year: bool = field(
        default=True,
        metadata={
            "name": "DisplayTheYear",
            "type": "Attribute",
        },
    )
