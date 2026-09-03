from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_resource_type_flavour import (
    HawkConfigurationDataResourcesResourceResourceTypeFlavour,
)


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataResourcesResourceResourceType:
    class Meta:
        global_type = False

    length: int = field(
        metadata={
            "name": "Length",
            "type": "Attribute",
        }
    )
    flavour: None | HawkConfigurationDataResourcesResourceResourceTypeFlavour = field(
        default=None,
        metadata={
            "name": "Flavour",
            "type": "Attribute",
        },
    )
