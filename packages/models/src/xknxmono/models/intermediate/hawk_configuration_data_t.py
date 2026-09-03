from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hawk_configuration_data_t_features import (
    HawkConfigurationDataFeatures,
)
from xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects import (
    HawkConfigurationDataInterfaceObjects,
)
from xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments import (
    HawkConfigurationDataMemorySegments,
)
from xknxmono.models.intermediate.hawk_configuration_data_t_procedures import (
    HawkConfigurationDataProcedures,
)
from xknxmono.models.intermediate.hawk_configuration_data_t_resources import (
    HawkConfigurationDataResources,
)


@dataclass(slots=True, kw_only=True)
class HawkConfigurationData:
    class Meta:
        name = "HawkConfigurationData_t"

    features: None | HawkConfigurationDataFeatures = field(
        default=None,
        metadata={
            "name": "Features",
            "type": "Element",
        },
    )
    resources: None | HawkConfigurationDataResources = field(
        default=None,
        metadata={
            "name": "Resources",
            "type": "Element",
        },
    )
    procedures: None | HawkConfigurationDataProcedures = field(
        default=None,
        metadata={
            "name": "Procedures",
            "type": "Element",
        },
    )
    memory_segments: None | HawkConfigurationDataMemorySegments = field(
        default=None,
        metadata={
            "name": "MemorySegments",
            "type": "Element",
        },
    )
    interface_objects: None | HawkConfigurationDataInterfaceObjects = field(
        default=None,
        metadata={
            "name": "InterfaceObjects",
            "type": "Element",
        },
    )
    ets3_system_plugin: None | str = field(
        default=None,
        metadata={
            "name": "Ets3SystemPlugin",
            "type": "Attribute",
            "pattern": r"\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}",
        },
    )
    legacy_version: None | int = field(
        default=None,
        metadata={
            "name": "LegacyVersion",
            "type": "Attribute",
        },
    )
