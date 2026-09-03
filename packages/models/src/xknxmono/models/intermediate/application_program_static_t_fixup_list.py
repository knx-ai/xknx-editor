from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.fixup_t import Fixup


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticFixupList:
    """
    :ivar fixup: registration-relevant set
    """

    class Meta:
        global_type = False

    fixup: list[Fixup] = field(
        default_factory=list,
        metadata={
            "name": "Fixup",
            "type": "Element",
            "min_occurs": 1,
        },
    )
