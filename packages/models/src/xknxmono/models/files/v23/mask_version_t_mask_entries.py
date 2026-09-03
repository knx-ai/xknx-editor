from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.mask_version_t_mask_entries_mask_entry import (
    MaskVersionMaskEntriesMaskEntry,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class MaskVersionMaskEntries:
    class Meta:
        global_type = False

    mask_entry: list[MaskVersionMaskEntriesMaskEntry] = field(
        default_factory=list,
        metadata={
            "name": "MaskEntry",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
