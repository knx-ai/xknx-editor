from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.com_object_parameter_block_t_columns_column import (
    ComObjectParameterBlockColumnsColumn,
)


@dataclass(slots=True, kw_only=True)
class ComObjectParameterBlockColumns:
    class Meta:
        global_type = False

    column: list[ComObjectParameterBlockColumnsColumn] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
