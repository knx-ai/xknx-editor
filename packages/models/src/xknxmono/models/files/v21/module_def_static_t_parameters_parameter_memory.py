from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.memory_parameter_t import MemoryParameter

__NAMESPACE__ = "http://knx.org/xml/project/21"


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
