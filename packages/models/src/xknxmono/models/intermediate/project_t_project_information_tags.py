from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.project_t_project_information_tags_tag import (
    ProjectProjectInformationTagsTag,
)


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationTags:
    class Meta:
        global_type = False

    tag: list[ProjectProjectInformationTagsTag] = field(
        default_factory=list,
        metadata={
            "name": "Tag",
            "type": "Element",
        },
    )
