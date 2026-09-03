from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.hawk_configuration_data_t_resources_resource import (
    HawkConfigurationDataResourcesResource,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataResources:
    class Meta:
        global_type = False

    resource: list[HawkConfigurationDataResourcesResource] = field(
        default_factory=list,
        metadata={
            "name": "Resource",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
