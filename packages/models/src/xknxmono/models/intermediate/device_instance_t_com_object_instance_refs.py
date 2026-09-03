from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.com_object_instance_ref_t import ComObjectInstanceRef


@dataclass(slots=True, kw_only=True)
class DeviceInstanceComObjectInstanceRefs:
    class Meta:
        global_type = False

    com_object_instance_ref: list[ComObjectInstanceRef] = field(
        default_factory=list,
        metadata={
            "name": "ComObjectInstanceRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )
