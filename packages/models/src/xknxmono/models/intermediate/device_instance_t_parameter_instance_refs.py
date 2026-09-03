from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.parameter_instance_ref_t import ParameterInstanceRef


@dataclass(slots=True, kw_only=True)
class DeviceInstanceParameterInstanceRefs:
    class Meta:
        global_type = False

    parameter_instance_ref: list[ParameterInstanceRef] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )
