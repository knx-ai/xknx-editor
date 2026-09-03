from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.project_t_project_information_tags_tag import (
    ProjectProjectInformationTagsTag,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationTags:
    class Meta:
        global_type = False

    tag: list[ProjectProjectInformationTagsTag] = field(
        default_factory=list,
        metadata={
            "name": "Tag",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
