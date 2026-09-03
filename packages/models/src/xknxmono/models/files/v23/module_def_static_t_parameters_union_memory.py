from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.memory_union_t import MemoryUnion

__NAMESPACE__ = "http://knx.org/xml/project/23"


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
