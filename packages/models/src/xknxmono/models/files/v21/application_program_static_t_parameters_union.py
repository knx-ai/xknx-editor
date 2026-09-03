from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.memory_union_t import MemoryUnion
from xknxmono.models.files.v21.property_union_t import PropertyUnion
from xknxmono.models.files.v21.union_parameter_t import UnionParameter

__NAMESPACE__ = "http://knx.org/xml/project/21"


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
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Property",
                    "type": PropertyUnion,
                    "namespace": "http://knx.org/xml/project/21",
                },
            ),
        },
    )
    parameter: list[UnionParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
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
