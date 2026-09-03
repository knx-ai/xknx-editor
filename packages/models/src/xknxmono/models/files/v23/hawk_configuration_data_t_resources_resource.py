from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.hawk_configuration_data_t_resources_resource_access_rights import (
    HawkConfigurationDataResourcesResourceAccessRights,
)
from xknxmono.models.files.v23.hawk_configuration_data_t_resources_resource_resource_type import (
    HawkConfigurationDataResourcesResourceResourceType,
)
from xknxmono.models.files.v23.resource_access_t import ResourceAccess
from xknxmono.models.files.v23.resource_location_t import ResourceLocation
from xknxmono.models.files.v23.resource_mgmt_style_t import ResourceMgmtStyle
from xknxmono.models.files.v23.resource_name_t import ResourceName

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataResourcesResource:
    class Meta:
        global_type = False

    location: None | ResourceLocation = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    img_location: None | ResourceLocation = field(
        default=None,
        metadata={
            "name": "ImgLocation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    resource_type: HawkConfigurationDataResourcesResourceResourceType = field(
        metadata={
            "name": "ResourceType",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        }
    )
    access_rights: HawkConfigurationDataResourcesResourceAccessRights = field(
        metadata={
            "name": "AccessRights",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
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
