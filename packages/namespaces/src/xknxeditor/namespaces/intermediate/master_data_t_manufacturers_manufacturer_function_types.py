from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.intermediate.function_type_t import FunctionType
from xknxeditor.namespaces.intermediate.functions_group_t import FunctionsGroup


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerFunctionTypes:
    class Meta:
        global_type = False

    functions_group: list[FunctionsGroup] = field(
        default_factory=list,
        metadata={
            "name": "FunctionsGroup",
            "type": "Element",
        },
    )
    function_type: list[FunctionType] = field(
        default_factory=list,
        metadata={
            "name": "FunctionType",
            "type": "Element",
        },
    )
