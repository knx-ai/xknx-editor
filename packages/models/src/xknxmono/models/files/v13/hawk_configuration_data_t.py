from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.hawk_configuration_data_t_features import (
    HawkConfigurationDataFeatures,
)
from xknxmono.models.files.v13.hawk_configuration_data_t_interface_objects import (
    HawkConfigurationDataInterfaceObjects,
)
from xknxmono.models.files.v13.hawk_configuration_data_t_memory_segments import (
    HawkConfigurationDataMemorySegments,
)
from xknxmono.models.files.v13.hawk_configuration_data_t_procedures import (
    HawkConfigurationDataProcedures,
)
from xknxmono.models.files.v13.hawk_configuration_data_t_resources import (
    HawkConfigurationDataResources,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationData:
    class Meta:
        name = "HawkConfigurationData_t"

    features: None | HawkConfigurationDataFeatures = field(
        default=None,
        metadata={
            "name": "Features",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
    resources: None | HawkConfigurationDataResources = field(
        default=None,
        metadata={
            "name": "Resources",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
    procedures: None | HawkConfigurationDataProcedures = field(
        default=None,
        metadata={
            "name": "Procedures",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
    memory_segments: None | HawkConfigurationDataMemorySegments = field(
        default=None,
        metadata={
            "name": "MemorySegments",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
    interface_objects: None | HawkConfigurationDataInterfaceObjects = field(
        default=None,
        metadata={
            "name": "InterfaceObjects",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
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
