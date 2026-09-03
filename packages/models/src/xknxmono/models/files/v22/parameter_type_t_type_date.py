from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.parameter_type_t_type_date_encoding import (
    ParameterTypeTypeDateEncoding,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


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
