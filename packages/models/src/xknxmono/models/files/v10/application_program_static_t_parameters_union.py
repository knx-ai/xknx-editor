from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.memory_union_t import MemoryUnion
from xknxmono.models.files.v10.property_union_t import PropertyUnion
from xknxmono.models.files.v10.union_parameter_t import UnionParameter

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParametersUnion:
    """
    :ivar choice:
    :ivar parameter: registration-relevant list This is a list to ensure deterministic
        behaviour in case of overlapping active parameters
    :ivar size_in_bit:
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
                    "namespace": "http://knx.org/xml/project/10",
                },
                {
                    "name": "Property",
                    "type": PropertyUnion,
                    "namespace": "http://knx.org/xml/project/10",
                },
            ),
        },
    )
    parameter: list[UnionParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
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
