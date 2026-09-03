from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.project_trace_t import ProjectTrace


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationProjectTraces:
    class Meta:
        global_type = False

    project_trace: list[ProjectTrace] = field(
        default_factory=list,
        metadata={
            "name": "ProjectTrace",
            "type": "Element",
            "min_occurs": 1,
        },
    )
