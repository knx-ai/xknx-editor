from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class Fixup:
    """
    :ivar offset: registration-relevant set
    :ivar function_ref: registration-relevant
    :ivar code_segment: registration-relevant
    """

    class Meta:
        name = "Fixup_t"

    offset: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
            "max_inclusive": 65535,
        },
    )
    function_ref: str = field(
        metadata={
            "name": "FunctionRef",
            "type": "Attribute",
        }
    )
    code_segment: str = field(
        metadata={
            "name": "CodeSegment",
            "type": "Attribute",
        }
    )
