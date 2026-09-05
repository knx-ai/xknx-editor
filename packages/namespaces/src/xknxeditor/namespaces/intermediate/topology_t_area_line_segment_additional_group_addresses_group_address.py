from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress:
    class Meta:
        global_type = False

    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
        }
    )
