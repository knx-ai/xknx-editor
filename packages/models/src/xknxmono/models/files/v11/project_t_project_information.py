from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

from xknxmono.models.files.v11.completion_status_t import CompletionStatus
from xknxmono.models.files.v11.group_address_style_t import GroupAddressStyle
from xknxmono.models.files.v11.project_t_project_information_history_entries import (
    ProjectProjectInformationHistoryEntries,
)
from xknxmono.models.files.v11.project_t_project_information_project_traces import (
    ProjectProjectInformationProjectTraces,
)
from xknxmono.models.files.v11.project_t_project_information_to_do_items import (
    ProjectProjectInformationToDoItems,
)
from xknxmono.models.files.v11.project_tracing_level_t import ProjectTracingLevel
from xknxmono.models.files.v11.text_encoding_t import TextEncoding

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformation:
    class Meta:
        global_type = False

    history_entries: None | ProjectProjectInformationHistoryEntries = field(
        default=None,
        metadata={
            "name": "HistoryEntries",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        },
    )
    to_do_items: None | ProjectProjectInformationToDoItems = field(
        default=None,
        metadata={
            "name": "ToDoItems",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        },
    )
    project_traces: None | ProjectProjectInformationProjectTraces = field(
        default=None,
        metadata={
            "name": "ProjectTraces",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        },
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    group_address_style: GroupAddressStyle = field(
        metadata={
            "name": "GroupAddressStyle",
            "type": "Attribute",
        }
    )
    project_number: None | str = field(
        default=None,
        metadata={
            "name": "ProjectNumber",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    contract_number: None | str = field(
        default=None,
        metadata={
            "name": "ContractNumber",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    last_modified: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "LastModified",
            "type": "Attribute",
        },
    )
    project_start: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "ProjectStart",
            "type": "Attribute",
        },
    )
    project_end: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "ProjectEnd",
            "type": "Attribute",
        },
    )
    project_id: None | int = field(
        default=None,
        metadata={
            "name": "ProjectId",
            "type": "Attribute",
            "max_inclusive": 4095,
        },
    )
    project_password: None | str = field(
        default=None,
        metadata={
            "name": "ProjectPassword",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    completion_status: CompletionStatus = field(
        default=CompletionStatus.UNDEFINED,
        metadata={
            "name": "CompletionStatus",
            "type": "Attribute",
        },
    )
    project_tracing_level: ProjectTracingLevel = field(
        default=ProjectTracingLevel.NONE,
        metadata={
            "name": "ProjectTracingLevel",
            "type": "Attribute",
        },
    )
    project_tracing_password: None | str = field(
        default=None,
        metadata={
            "name": "ProjectTracingPassword",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    hide16_bit_groups_from_legacy_plugins: bool = field(
        default=False,
        metadata={
            "name": "Hide16BitGroupsFromLegacyPlugins",
            "type": "Attribute",
        },
    )
    code_page: None | TextEncoding = field(
        default=None,
        metadata={
            "name": "CodePage",
            "type": "Attribute",
        },
    )
