from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.project_t_installations_installation import (
    ProjectInstallationsInstallation,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ProjectInstallations:
    class Meta:
        global_type = False

    installation: list[ProjectInstallationsInstallation] = field(
        default_factory=list,
        metadata={
            "name": "Installation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
            "max_occurs": 16,
        },
    )
