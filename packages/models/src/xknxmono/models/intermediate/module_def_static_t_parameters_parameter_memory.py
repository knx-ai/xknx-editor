from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.memory_parameter_t import MemoryParameter


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParametersParameterMemory(MemoryParameter):
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
