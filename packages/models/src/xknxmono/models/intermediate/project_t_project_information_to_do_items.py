from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.to_do_item_t import ToDoItem


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationToDoItems:
    class Meta:
        global_type = False

    to_do_item: list[ToDoItem] = field(
        default_factory=list,
        metadata={
            "name": "ToDoItem",
            "type": "Element",
            "min_occurs": 1,
        },
    )
