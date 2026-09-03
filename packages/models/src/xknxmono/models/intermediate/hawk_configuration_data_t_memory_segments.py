from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments_memory_segment import (
    HawkConfigurationDataMemorySegmentsMemorySegment,
)


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataMemorySegments:
    class Meta:
        global_type = False

    memory_segment: list[HawkConfigurationDataMemorySegmentsMemorySegment] = field(
        default_factory=list,
        metadata={
            "name": "MemorySegment",
            "type": "Element",
            "min_occurs": 1,
        },
    )
