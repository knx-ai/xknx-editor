from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.module_instance_t import ModuleInstance

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceModuleInstances:
    class Meta:
        global_type = False

    module_instance: list[ModuleInstance] = field(
        default_factory=list,
        metadata={
            "name": "ModuleInstance",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
