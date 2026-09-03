from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.mask_version_t import MaskVersion

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class MasterDataMaskVersions:
    class Meta:
        global_type = False

    mask_version: list[MaskVersion] = field(
        default_factory=list,
        metadata={
            "name": "MaskVersion",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
