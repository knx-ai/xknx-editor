from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.module_def_static_t_com_objects_com_object import (
    ModuleDefStaticComObjectsComObject,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticComObjects:
    """
    :ivar com_object: registration-relevant set
    """

    class Meta:
        global_type = False

    com_object: list[ModuleDefStaticComObjectsComObject] = field(
        default_factory=list,
        metadata={
            "name": "ComObject",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
