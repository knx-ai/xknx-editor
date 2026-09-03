from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.deprecation_status_t import DeprecationStatus
from xknxmono.models.intermediate.function_type_t_function_point import (
    FunctionTypeFunctionPoint,
)


@dataclass(slots=True, kw_only=True)
class FunctionType:
    class Meta:
        name = "FunctionType_t"

    function_point: list[FunctionTypeFunctionPoint] = field(
        default_factory=list,
        metadata={
            "name": "FunctionPoint",
            "type": "Element",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    status: DeprecationStatus = field(
        default=DeprecationStatus.ACTIVE,
        metadata={
            "name": "Status",
            "type": "Attribute",
        },
    )
    semantics: None | str = field(
        default=None,
        metadata={
            "name": "Semantics",
            "type": "Attribute",
        },
    )
