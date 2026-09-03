from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.module_def_t import ModuleDef

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramModuleDefs:
    """
    :ivar module_def: registration-relevant set
    """

    class Meta:
        global_type = False

    module_def: list[ModuleDef] = field(
        default_factory=list,
        metadata={
            "name": "ModuleDef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
