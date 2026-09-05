from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticExtensionBaggage:
    class Meta:
        global_type = False

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
