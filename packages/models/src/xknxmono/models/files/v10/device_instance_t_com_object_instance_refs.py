from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.com_object_instance_ref_t import ComObjectInstanceRef

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceComObjectInstanceRefs:
    class Meta:
        global_type = False

    com_object_instance_ref: list[ComObjectInstanceRef] = field(
        default_factory=list,
        metadata={
            "name": "ComObjectInstanceRef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
