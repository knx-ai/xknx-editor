from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hawk_configuration_data_t_features_feature import (
    HawkConfigurationDataFeaturesFeature,
)


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataFeatures:
    class Meta:
        global_type = False

    feature: list[HawkConfigurationDataFeaturesFeature] = field(
        default_factory=list,
        metadata={
            "name": "Feature",
            "type": "Element",
            "min_occurs": 1,
        },
    )
