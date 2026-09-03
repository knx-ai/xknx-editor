from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.application_program_static_t_device_compare_exclude_memory import (
    ApplicationProgramStaticDeviceCompareExcludeMemory,
)
from xknxmono.models.files.v10.application_program_static_t_device_compare_exclude_property import (
    ApplicationProgramStaticDeviceCompareExcludeProperty,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticDeviceCompare:
    class Meta:
        global_type = False

    exclude_memory: list[ApplicationProgramStaticDeviceCompareExcludeMemory] = field(
        default_factory=list,
        metadata={
            "name": "ExcludeMemory",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    exclude_property: list[ApplicationProgramStaticDeviceCompareExcludeProperty] = (
        field(
            default_factory=list,
            metadata={
                "name": "ExcludeProperty",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/10",
            },
        )
    )
