from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.master_data_t_functional_blocks_functional_block import (
    MasterDataFunctionalBlocksFunctionalBlock,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class MasterDataFunctionalBlocks:
    class Meta:
        global_type = False

    functional_block: list[MasterDataFunctionalBlocksFunctionalBlock] = field(
        default_factory=list,
        metadata={
            "name": "FunctionalBlock",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
