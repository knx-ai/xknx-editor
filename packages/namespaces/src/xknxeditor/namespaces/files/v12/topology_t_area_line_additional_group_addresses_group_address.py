from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class TopologyAreaLineAdditionalGroupAddressesGroupAddress:
    class Meta:
        global_type = False

    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
        }
    )
