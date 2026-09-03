from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block_parameters_parameter import (
    MasterDataFunctionalBlocksFunctionalBlockParametersParameter,
)


@dataclass(slots=True, kw_only=True)
class MasterDataFunctionalBlocksFunctionalBlockParameters:
    class Meta:
        global_type = False

    parameter: list[MasterDataFunctionalBlocksFunctionalBlockParametersParameter] = (
        field(
            default_factory=list,
            metadata={
                "name": "Parameter",
                "type": "Element",
            },
        )
    )
    object_type: str = field(
        metadata={
            "name": "ObjectType",
            "type": "Attribute",
        }
    )
