from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.hawk_configuration_data_t_memory_segments_memory_segment_access_rights import (
    HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights,
)
from xknxmono.models.files.v12.memory_type_t import MemoryType
from xknxmono.models.files.v12.resource_location_t import ResourceLocation

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataMemorySegmentsMemorySegment:
    class Meta:
        global_type = False

    location: ResourceLocation = field(
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        }
    )
    access_rights: HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights = field(
        metadata={
            "name": "AccessRights",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        }
    )
    length: int = field(
        metadata={
            "name": "Length",
            "type": "Attribute",
        }
    )
    optional: bool = field(
        default=False,
        metadata={
            "name": "Optional",
            "type": "Attribute",
        },
    )
    memory_type: None | MemoryType = field(
        default=None,
        metadata={
            "name": "MemoryType",
            "type": "Attribute",
        },
    )
