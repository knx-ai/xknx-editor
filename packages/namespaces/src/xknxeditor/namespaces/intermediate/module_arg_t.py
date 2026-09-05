from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ModuleArg:
    """
    :ivar ref_id: registration-relevant
    """

    class Meta:
        name = "ModuleArg_t"

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
