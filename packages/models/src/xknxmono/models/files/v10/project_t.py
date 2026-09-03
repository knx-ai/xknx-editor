from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.project_t_add_in_data import ProjectAddInData
from xknxmono.models.files.v10.project_t_installations import ProjectInstallations
from xknxmono.models.files.v10.project_t_project_information import (
    ProjectProjectInformation,
)
from xknxmono.models.files.v10.project_t_user_files import ProjectUserFiles

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class Project:
    class Meta:
        name = "Project_t"

    project_information: None | ProjectProjectInformation = field(
        default=None,
        metadata={
            "name": "ProjectInformation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    installations: None | ProjectInstallations = field(
        default=None,
        metadata={
            "name": "Installations",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    user_files: None | ProjectUserFiles = field(
        default=None,
        metadata={
            "name": "UserFiles",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    add_in_data: None | ProjectAddInData = field(
        default=None,
        metadata={
            "name": "AddInData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
