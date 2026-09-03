from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.deprecation_status_t import DeprecationStatus
from xknxmono.models.intermediate.function_type_t import FunctionType


@dataclass(slots=True, kw_only=True)
class FunctionsGroup:
    class Meta:
        name = "FunctionsGroup_t"

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
