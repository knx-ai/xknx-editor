from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class IoPointParameter:
    """
    :ivar point_reference: registration-relevant
    """

    class Meta:
        name = "IoTPointParameter_t"

    point_reference: str = field(
        metadata={
            "name": "PointReference",
            "type": "Attribute",
        }
    )
