from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.load_procedure_t import LoadProcedure


@dataclass(slots=True, kw_only=True)
class LoadProceduresLoadProcedure(LoadProcedure):
    """
    :ivar merge_id: registration-relevant
    """

    class Meta:
        global_type = False

    merge_id: None | int = field(
        default=None,
        metadata={
            "name": "MergeId",
            "type": "Attribute",
        },
    )
