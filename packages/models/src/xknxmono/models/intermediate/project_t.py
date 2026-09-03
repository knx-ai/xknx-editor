from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.project_t_addin_data import ProjectAddinData
from xknxmono.models.intermediate.project_t_installations import ProjectInstallations
from xknxmono.models.intermediate.project_t_project_information import (
    ProjectProjectInformation,
)
from xknxmono.models.intermediate.project_t_user_files import ProjectUserFiles


@dataclass(slots=True, kw_only=True)
class Project:
    class Meta:
        name = "Project_t"

    project_information: None | ProjectProjectInformation = field(
        default=None,
        metadata={
            "name": "ProjectInformation",
            "type": "Element",
        },
    )
    installations: None | ProjectInstallations = field(
        default=None,
        metadata={
            "name": "Installations",
            "type": "Element",
        },
    )
    user_files: None | ProjectUserFiles = field(
        default=None,
        metadata={
            "name": "UserFiles",
            "type": "Element",
        },
    )
    addin_data: None | ProjectAddinData = field(
        default=None,
        metadata={
            "name": "AddinData",
            "type": "Element",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
