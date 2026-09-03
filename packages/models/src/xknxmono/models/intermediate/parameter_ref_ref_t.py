from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ParameterRefRef:
    """
    :ivar ref_id: registration-relevant
    :ivar indent_level:
    :ivar internal_description:
    :ivar help_context:
    :ivar cell:
    :ivar icon:
    """

    class Meta:
        name = "ParameterRefRef_t"

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    indent_level: int = field(
        default=0,
        metadata={
            "name": "IndentLevel",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    help_context: None | str = field(
        default=None,
        metadata={
            "name": "HelpContext",
            "type": "Attribute",
        },
    )
    cell: None | str = field(
        default=None,
        metadata={
            "name": "Cell",
            "type": "Attribute",
            "pattern": r"\d+,\d+",
        },
    )
    icon: None | str = field(
        default=None,
        metadata={
            "name": "Icon",
            "type": "Attribute",
        },
    )
