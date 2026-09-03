from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.fixup_t import Fixup

__NAMESPACE__ = "http://knx.org/xml/project/23"


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
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
