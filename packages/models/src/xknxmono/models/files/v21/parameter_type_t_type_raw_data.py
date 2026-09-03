from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeRawData:
    """
    :ivar max_size: registration-relevant
    """

    class Meta:
        global_type = False

    max_size: int = field(
        metadata={
            "name": "MaxSize",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 1048572,
        }
    )
