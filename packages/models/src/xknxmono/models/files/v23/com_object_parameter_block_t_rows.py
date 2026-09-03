from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.com_object_parameter_block_t_rows_row import (
    ComObjectParameterBlockRowsRow,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ComObjectParameterBlockRows:
    class Meta:
        global_type = False

    row: list[ComObjectParameterBlockRowsRow] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
