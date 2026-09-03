from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.memory_union_t import MemoryUnion
from xknxmono.models.intermediate.property_union_t import PropertyUnion
from xknxmono.models.intermediate.union_parameter_t import UnionParameter


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParametersUnion:
    """
    :ivar choice:
    :ivar parameter: registration-relevant set
    :ivar size_in_bit:
    :ivar internal_description:
    """

    class Meta:
        global_type = False

    choice: None | MemoryUnion | PropertyUnion = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Memory",
                    "type": MemoryUnion,
                },
                {
                    "name": "Property",
                    "type": PropertyUnion,
                },
            ),
        },
    )
    parameter: list[UnionParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    size_in_bit: int = field(
        metadata={
            "name": "SizeInBit",
            "type": "Attribute",
            "max_inclusive": 8388600,
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
