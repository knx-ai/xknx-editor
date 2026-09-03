from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.project_t_addin_data import ProjectAddinData
from xknxmono.models.files.v20.project_t_installations import ProjectInstallations
from xknxmono.models.files.v20.project_t_project_information import (
    ProjectProjectInformation,
)
from xknxmono.models.files.v20.project_t_user_files import ProjectUserFiles

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class Project:
    class Meta:
        name = "Project_t"

    project_information: None | ProjectProjectInformation = field(
        default=None,
        metadata={
            "name": "ProjectInformation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    installations: None | ProjectInstallations = field(
        default=None,
        metadata={
            "name": "Installations",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    user_files: None | ProjectUserFiles = field(
        default=None,
        metadata={
            "name": "UserFiles",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    addin_data: None | ProjectAddinData = field(
        default=None,
        metadata={
            "name": "AddinData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
