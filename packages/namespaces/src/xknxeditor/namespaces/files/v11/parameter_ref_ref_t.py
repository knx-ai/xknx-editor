from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ParameterRefRef:
    """
    :ivar ref_id: registration-relevant
    """

    class Meta:
        name = "ParameterRefRef_t"

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
