from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_instance_t_arguments import (
    ModuleInstanceArguments,
)


@dataclass(slots=True, kw_only=True)
class ModuleInstance:
    class Meta:
        name = "ModuleInstance_t"

    arguments: None | ModuleInstanceArguments = field(
        default=None,
        metadata={
            "name": "Arguments",
            "type": "Element",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        },
    )
    ref_id: None | str = field(
        default=None,
        metadata={
            "name": "RefId",
            "type": "Attribute",
        },
    )
    repeat_index: list[str] = field(
        default_factory=list,
        metadata={
            "name": "RepeatIndex",
            "type": "Attribute",
            "pattern": r"\d+x\d+",
            "tokens": True,
        },
    )
