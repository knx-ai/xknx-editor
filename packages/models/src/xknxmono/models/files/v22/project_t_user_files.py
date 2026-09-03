from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.user_file_t import UserFile

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ProjectUserFiles:
    class Meta:
        global_type = False

    user_file: list[UserFile] = field(
        default_factory=list,
        metadata={
            "name": "UserFile",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
