from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticDeviceCompareExcludeProperty:
    class Meta:
        global_type = False

    object_index: None | int = field(
        default=None,
        metadata={
            "name": "ObjectIndex",
            "type": "Attribute",
        },
    )
    object_type: None | int = field(
        default=None,
        metadata={
            "name": "ObjectType",
            "type": "Attribute",
        },
    )
    occurrence: int = field(
        default=0,
        metadata={
            "name": "Occurrence",
            "type": "Attribute",
        },
    )
    property_id: int = field(
        metadata={
            "name": "PropertyId",
            "type": "Attribute",
        }
    )
    offset: int = field(
        metadata={
            "name": "Offset",
            "type": "Attribute",
        }
    )
    size: int = field(
        metadata={
            "name": "Size",
            "type": "Attribute",
            "max_inclusive": 1048575,
        }
    )
