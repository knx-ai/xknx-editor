from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ComObjectRefRef:
    """
    :ivar ref_id: registration-relevant
    """

    class Meta:
        name = "ComObjectRefRef_t"

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
