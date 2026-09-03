from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.project_t_project_information_history_entries_history_entry import (
    ProjectProjectInformationHistoryEntriesHistoryEntry,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationHistoryEntries:
    class Meta:
        global_type = False

    history_entry: list[ProjectProjectInformationHistoryEntriesHistoryEntry] = field(
        default_factory=list,
        metadata={
            "name": "HistoryEntry",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
