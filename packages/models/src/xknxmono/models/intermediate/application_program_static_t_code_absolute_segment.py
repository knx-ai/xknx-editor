from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.memory_type_t import MemoryType
from xknxmono.models.intermediate.segment_base_t import SegmentBase


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticCodeAbsoluteSegment(SegmentBase):
    """
    :ivar memory_type:
    :ivar address: registration-relevant
    :ivar user_memory: registration-relevant
    """

    class Meta:
        global_type = False

    memory_type: None | MemoryType = field(
        default=None,
        metadata={
            "name": "MemoryType",
            "type": "Attribute",
        },
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
            "max_inclusive": 1048575,
        }
    )
    user_memory: bool = field(
        default=False,
        metadata={
            "name": "UserMemory",
            "type": "Attribute",
        },
    )
