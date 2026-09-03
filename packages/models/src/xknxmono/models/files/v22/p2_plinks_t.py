from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.p2_plinks_t_p2_plink import P2PlinksP2Plink

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class P2Plinks:
    class Meta:
        name = "P2PLinks_t"

    p2_plink: list[P2PlinksP2Plink] = field(
        default_factory=list,
        metadata={
            "name": "P2PLink",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
