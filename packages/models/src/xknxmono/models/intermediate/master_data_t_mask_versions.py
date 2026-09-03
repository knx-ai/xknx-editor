from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.mask_version_t import MaskVersion


@dataclass(slots=True, kw_only=True)
class MasterDataMaskVersions:
    class Meta:
        global_type = False

    mask_version: list[MaskVersion] = field(
        default_factory=list,
        metadata={
            "name": "MaskVersion",
            "type": "Element",
            "min_occurs": 1,
        },
    )
