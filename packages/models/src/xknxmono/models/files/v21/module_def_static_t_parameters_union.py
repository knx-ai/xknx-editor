from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.module_def_static_t_parameters_union_memory import (
    ModuleDefStaticParametersUnionMemory,
)
from xknxmono.models.files.v21.module_def_static_t_parameters_union_property import (
    ModuleDefStaticParametersUnionProperty,
)
from xknxmono.models.files.v21.union_parameter_t import UnionParameter

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParametersUnion:
    """
    :ivar choice:
    :ivar parameter: registration-relevant set
    :ivar size_in_bit:
    """

    class Meta:
        global_type = False

    choice: (
        None
        | ModuleDefStaticParametersUnionMemory
        | ModuleDefStaticParametersUnionProperty
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Memory",
                    "type": ModuleDefStaticParametersUnionMemory,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "Property",
                    "type": ModuleDefStaticParametersUnionProperty,
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
