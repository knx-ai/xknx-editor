from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.load_procedure_t import LoadProcedure

__NAMESPACE__ = "http://knx.org/xml/project/11"


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
