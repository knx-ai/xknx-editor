from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments_memory_segment_access_rights import (
    HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights,
)
from xknxmono.models.intermediate.memory_type_t import MemoryType
from xknxmono.models.intermediate.resource_location_t import ResourceLocation


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataMemorySegmentsMemorySegment:
    class Meta:
        global_type = False

    location: None | ResourceLocation = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
        },
    )
    access_rights: HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights = field(
        metadata={
            "name": "AccessRights",
            "type": "Element",
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
