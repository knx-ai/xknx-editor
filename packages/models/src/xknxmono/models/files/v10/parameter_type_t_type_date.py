from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.parameter_type_t_type_date_encoding import (
    ParameterTypeTypeDateEncoding,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeDate:
    """
    :ivar encoding: registration-relevant
    """

    class Meta:
        global_type = False

    encoding: ParameterTypeTypeDateEncoding = field(
        metadata={
            "name": "Encoding",
            "type": "Attribute",
        }
    )
