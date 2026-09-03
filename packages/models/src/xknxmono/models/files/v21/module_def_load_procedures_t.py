from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.module_def_load_procedure_t import ModuleDefLoadProcedure

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ModuleDefLoadProcedures:
    """
    :ivar load_procedure: registration-relevant set
    """

    class Meta:
        name = "ModuleDefLoadProcedures_t"

    load_procedure: list[ModuleDefLoadProcedure] = field(
        default_factory=list,
        metadata={
            "name": "LoadProcedure",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
