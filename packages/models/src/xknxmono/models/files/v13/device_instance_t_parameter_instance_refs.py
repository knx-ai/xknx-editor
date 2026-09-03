from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.parameter_instance_ref_t import ParameterInstanceRef

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceParameterInstanceRefs:
    class Meta:
        global_type = False

    parameter_instance_ref: list[ParameterInstanceRef] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "min_occurs": 1,
        },
    )
