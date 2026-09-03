from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.mask_version_t_downward_compatible_masks_downward_compatible_mask import (
    MaskVersionDownwardCompatibleMasksDownwardCompatibleMask,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class MaskVersionDownwardCompatibleMasks:
    class Meta:
        global_type = False

    downward_compatible_mask: list[
        MaskVersionDownwardCompatibleMasksDownwardCompatibleMask
    ] = field(
        default_factory=list,
        metadata={
            "name": "DownwardCompatibleMask",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
