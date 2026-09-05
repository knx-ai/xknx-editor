from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/23"


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
