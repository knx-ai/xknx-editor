from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.deprecation_status_t import DeprecationStatus

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class DatapointRole:
    class Meta:
        name = "DatapointRole_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
    status: DeprecationStatus = field(
        default=DeprecationStatus.ACTIVE,
        metadata={
            "name": "Status",
            "type": "Attribute",
        },
    )
    semantics: None | str = field(
        default=None,
        metadata={
            "name": "Semantics",
            "type": "Attribute",
        },
    )
