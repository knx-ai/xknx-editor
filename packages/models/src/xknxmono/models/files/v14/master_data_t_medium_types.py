from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.master_data_t_medium_types_medium_type import (
    MasterDataMediumTypesMediumType,
)

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class MasterDataMediumTypes:
    class Meta:
        global_type = False

    medium_type: list[MasterDataMediumTypesMediumType] = field(
        default_factory=list,
        metadata={
            "name": "MediumType",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
