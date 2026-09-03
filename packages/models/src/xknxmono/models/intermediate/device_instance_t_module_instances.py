from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.module_instance_t import ModuleInstance


@dataclass(slots=True, kw_only=True)
class DeviceInstanceModuleInstances:
    class Meta:
        global_type = False

    module_instance: list[ModuleInstance] = field(
        default_factory=list,
        metadata={
            "name": "ModuleInstance",
            "type": "Element",
        },
    )
