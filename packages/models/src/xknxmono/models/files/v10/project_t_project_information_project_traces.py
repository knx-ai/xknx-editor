from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.project_trace_t import ProjectTrace

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationProjectTraces:
    class Meta:
        global_type = False

    project_trace: ProjectTrace = field(
        metadata={
            "name": "ProjectTrace",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        }
    )
