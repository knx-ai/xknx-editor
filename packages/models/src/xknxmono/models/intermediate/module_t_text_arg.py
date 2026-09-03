from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_arg_t import ModuleArg


@dataclass(slots=True, kw_only=True)
class ModuleTextArg(ModuleArg):
    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    value: str = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
            "max_length": 255,
        }
    )
