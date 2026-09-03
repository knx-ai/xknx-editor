from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.hawk_configuration_data_t_memory_segments_memory_segment import (
    HawkConfigurationDataMemorySegmentsMemorySegment,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataMemorySegments:
    class Meta:
        global_type = False

    memory_segment: list[HawkConfigurationDataMemorySegmentsMemorySegment] = field(
        default_factory=list,
        metadata={
            "name": "MemorySegment",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "min_occurs": 1,
        },
    )
