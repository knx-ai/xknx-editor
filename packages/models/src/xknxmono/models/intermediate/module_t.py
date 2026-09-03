from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.module_t_numeric_arg import ModuleNumericArg
from xknxmono.models.intermediate.module_t_text_arg import ModuleTextArg


@dataclass(slots=True, kw_only=True)
class Module:
    """
    :ivar choice:
    :ivar id:
    :ivar ref_id: registration-relevant
    :ivar name:
    :ivar internal_description:
    """

    class Meta:
        name = "Module_t"

    choice: list[ModuleNumericArg | ModuleTextArg] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "NumericArg",
                    "type": ModuleNumericArg,
                },
                {
                    "name": "TextArg",
                    "type": ModuleTextArg,
                },
            ),
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
