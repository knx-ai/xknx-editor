from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.to_do_item_t import ToDoItem

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationToDoItems:
    class Meta:
        global_type = False

    to_do_item: list[ToDoItem] = field(
        default_factory=list,
        metadata={
            "name": "ToDoItem",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
