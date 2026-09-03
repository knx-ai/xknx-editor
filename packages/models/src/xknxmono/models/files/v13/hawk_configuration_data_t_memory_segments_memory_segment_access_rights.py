from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.resource_access_rights_t import ResourceAccessRights

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights:
    class Meta:
        global_type = False

    read: ResourceAccessRights = field(
        metadata={
            "name": "Read",
            "type": "Attribute",
        }
    )
    write: ResourceAccessRights = field(
        metadata={
            "name": "Write",
            "type": "Attribute",
        }
    )
