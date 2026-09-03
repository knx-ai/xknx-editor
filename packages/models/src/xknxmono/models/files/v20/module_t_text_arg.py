from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.module_arg_t import ModuleArg

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
