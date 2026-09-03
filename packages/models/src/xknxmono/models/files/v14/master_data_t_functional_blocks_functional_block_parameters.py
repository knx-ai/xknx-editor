from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.master_data_t_functional_blocks_functional_block_parameters_parameter import (
    MasterDataFunctionalBlocksFunctionalBlockParametersParameter,
)

__NAMESPACE__ = "http://knx.org/xml/project/14"


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
                "namespace": "http://knx.org/xml/project/14",
                "min_occurs": 1,
            },
        )
    )
    object_type: str = field(
        metadata={
            "name": "ObjectType",
            "type": "Attribute",
        }
    )
