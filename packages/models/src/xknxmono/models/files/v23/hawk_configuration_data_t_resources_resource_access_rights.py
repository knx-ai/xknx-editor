from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.resource_access_rights_t import ResourceAccessRights

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataResourcesResourceAccessRights:
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
