from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class MemoryParameter:
    """
    :ivar code_segment: registration-relevant
    :ivar offset: registration-relevant
    :ivar bit_offset: registration-relevant
    """

    class Meta:
        name = "MemoryParameter_t"

    code_segment: str = field(
        metadata={
            "name": "CodeSegment",
            "type": "Attribute",
        }
    )
    offset: int = field(
        metadata={
            "name": "Offset",
            "type": "Attribute",
            "max_inclusive": 1048575,
        }
    )
    bit_offset: int = field(
        metadata={
            "name": "BitOffset",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 7,
        }
    )
