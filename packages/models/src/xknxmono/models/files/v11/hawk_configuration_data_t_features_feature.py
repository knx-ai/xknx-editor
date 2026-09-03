from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.hawk_configuration_data_t_features_feature_name import (
    HawkConfigurationDataFeaturesFeatureName,
)

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataFeaturesFeature:
    class Meta:
        global_type = False

    name: HawkConfigurationDataFeaturesFeatureName = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    value: int = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
