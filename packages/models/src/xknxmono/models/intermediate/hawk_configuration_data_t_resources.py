from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource import (
    HawkConfigurationDataResourcesResource,
)


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataResources:
    class Meta:
        global_type = False

    resource: list[HawkConfigurationDataResourcesResource] = field(
        default_factory=list,
        metadata={
            "name": "Resource",
            "type": "Element",
            "min_occurs": 1,
        },
    )
