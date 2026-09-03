from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.to_do_item_t import ToDoItem

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationToDoItems:
    class Meta:
        global_type = False

    to_do_item: ToDoItem = field(
        metadata={
            "name": "ToDoItem",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        }
    )
