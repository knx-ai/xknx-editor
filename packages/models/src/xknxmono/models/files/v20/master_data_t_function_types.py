from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.function_type_t import FunctionType
from xknxmono.models.files.v20.functions_group_t import FunctionsGroup

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class MasterDataFunctionTypes:
    class Meta:
        global_type = False

    functions_group: list[FunctionsGroup] = field(
        default_factory=list,
        metadata={
            "name": "FunctionsGroup",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    function_type: list[FunctionType] = field(
        default_factory=list,
        metadata={
            "name": "FunctionType",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
