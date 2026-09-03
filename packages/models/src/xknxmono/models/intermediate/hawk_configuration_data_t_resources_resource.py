from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_access_rights import (
    HawkConfigurationDataResourcesResourceAccessRights,
)
from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_resource_type import (
    HawkConfigurationDataResourcesResourceResourceType,
)
from xknxmono.models.intermediate.resource_access_t import ResourceAccess
from xknxmono.models.intermediate.resource_location_t import ResourceLocation
from xknxmono.models.intermediate.resource_mgmt_style_t import ResourceMgmtStyle
from xknxmono.models.intermediate.resource_name_t import ResourceName


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataResourcesResource:
    class Meta:
        global_type = False

    location: None | ResourceLocation = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
        },
    )
    img_location: None | ResourceLocation = field(
        default=None,
        metadata={
            "name": "ImgLocation",
            "type": "Element",
        },
    )
    resource_type: HawkConfigurationDataResourcesResourceResourceType = field(
        metadata={
            "name": "ResourceType",
            "type": "Element",
        }
    )
    access_rights: HawkConfigurationDataResourcesResourceAccessRights = field(
        metadata={
            "name": "AccessRights",
            "type": "Element",
        }
    )
    name: ResourceName = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    access: list[ResourceAccess] = field(
        default_factory=list,
        metadata={
            "name": "Access",
            "type": "Attribute",
            "tokens": True,
        },
    )
    mgmt_style: list[ResourceMgmtStyle] = field(
        default_factory=list,
        metadata={
            "name": "MgmtStyle",
            "type": "Attribute",
            "tokens": True,
        },
    )
    optional: bool = field(
        default=False,
        metadata={
            "name": "Optional",
            "type": "Attribute",
        },
    )
