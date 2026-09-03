from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.load_procedures_t_load_procedure import (
    LoadProceduresLoadProcedure,
)


@dataclass(slots=True, kw_only=True)
class LoadProcedures:
    """
    :ivar load_procedure: registration-relevant set
    """

    class Meta:
        name = "LoadProcedures_t"

    load_procedure: list[LoadProceduresLoadProcedure] = field(
        default_factory=list,
        metadata={
            "name": "LoadProcedure",
            "type": "Element",
            "min_occurs": 1,
        },
    )
