from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.hawk_configuration_data_t_features_feature import (
    HawkConfigurationDataFeaturesFeature,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataFeatures:
    class Meta:
        global_type = False

    feature: list[HawkConfigurationDataFeaturesFeature] = field(
        default_factory=list,
        metadata={
            "name": "Feature",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
