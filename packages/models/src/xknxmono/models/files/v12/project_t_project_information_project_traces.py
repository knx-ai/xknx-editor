from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.project_trace_t import ProjectTrace

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationProjectTraces:
    class Meta:
        global_type = False

    project_trace: list[ProjectTrace] = field(
        default_factory=list,
        metadata={
            "name": "ProjectTrace",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
