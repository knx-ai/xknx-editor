from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_device_compare_exclude_memory import (
    ApplicationProgramStaticDeviceCompareExcludeMemory,
)
from xknxmono.models.intermediate.application_program_static_t_device_compare_exclude_property import (
    ApplicationProgramStaticDeviceCompareExcludeProperty,
)
from xknxmono.models.intermediate.com_table_expectation_t import ComTableExpectation


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticDeviceCompare:
    class Meta:
        global_type = False

    exclude_memory: list[ApplicationProgramStaticDeviceCompareExcludeMemory] = field(
        default_factory=list,
        metadata={
            "name": "ExcludeMemory",
            "type": "Element",
        },
    )
    exclude_property: list[ApplicationProgramStaticDeviceCompareExcludeProperty] = (
        field(
            default_factory=list,
            metadata={
                "name": "ExcludeProperty",
                "type": "Element",
            },
        )
    )
    standard_com_tables_expectable: ComTableExpectation = field(
        default=ComTableExpectation.TRY,
        metadata={
            "name": "StandardComTablesExpectable",
            "type": "Attribute",
        },
    )
