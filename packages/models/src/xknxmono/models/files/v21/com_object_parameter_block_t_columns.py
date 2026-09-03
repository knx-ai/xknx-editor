from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.com_object_parameter_block_t_columns_column import (
    ComObjectParameterBlockColumnsColumn,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ComObjectParameterBlockColumns:
    class Meta:
        global_type = False

    column: list[ComObjectParameterBlockColumnsColumn] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
