from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class MasterDataFunctionalBlocksFunctionalBlockParametersParameter:
    class Meta:
        global_type = False

    property: str = field(
        metadata={
            "name": "Property",
            "type": "Attribute",
        }
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
