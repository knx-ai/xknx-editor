from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.master_data_t_functional_blocks_functional_block_parameters import (
    MasterDataFunctionalBlocksFunctionalBlockParameters,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class MasterDataFunctionalBlocksFunctionalBlock:
    class Meta:
        global_type = False

    parameters: list[MasterDataFunctionalBlocksFunctionalBlockParameters] = field(
        default_factory=list,
        metadata={
            "name": "Parameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
