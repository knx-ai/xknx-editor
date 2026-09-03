from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.to_do_status_t import ToDoStatus


@dataclass(slots=True, kw_only=True)
class ToDoItem:
    class Meta:
        name = "ToDoItem_t"

    description: str = field(
        metadata={
            "name": "Description",
            "type": "Attribute",
        }
    )
    object_path: None | str = field(
        default=None,
        metadata={
            "name": "ObjectPath",
            "type": "Attribute",
        },
    )
    status: ToDoStatus = field(
        metadata={
            "name": "Status",
            "type": "Attribute",
        }
    )
