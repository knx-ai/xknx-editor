from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.fixup_t import Fixup

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
