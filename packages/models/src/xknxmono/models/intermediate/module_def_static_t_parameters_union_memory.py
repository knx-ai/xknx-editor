from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.memory_union_t import MemoryUnion


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParametersUnionMemory(MemoryUnion):
    """
    :ivar base_offset: registration-relevant
    """

    class Meta:
        global_type = False

    base_offset: None | str = field(
        default=None,
        metadata={
            "name": "BaseOffset",
            "type": "Attribute",
        },
    )
