from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.com_object_ref_t import ComObjectRef

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticComObjectRefs:
    """
    :ivar com_object_ref: registration-relevant set This is a list to ensure deterministic
        behaviour in case of multiple active communication object refs
    """

    class Meta:
        global_type = False

    com_object_ref: list[ComObjectRef] = field(
        default_factory=list,
        metadata={
            "name": "ComObjectRef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
