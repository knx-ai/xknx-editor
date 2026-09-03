from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.module_instance_t_arguments import (
    ModuleInstanceArguments,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ModuleInstance:
    class Meta:
        name = "ModuleInstance_t"

    arguments: None | ModuleInstanceArguments = field(
        default=None,
        metadata={
            "name": "Arguments",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
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
