from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.bus_access_t import BusAccess
from xknxmono.models.files.v11.completion_status_t import CompletionStatus
from xknxmono.models.files.v11.group_addresses_t import GroupAddresses
from xknxmono.models.files.v11.locations_t import Locations
from xknxmono.models.files.v11.project_t_installations_installation_split_type import (
    ProjectInstallationsInstallationSplitType,
)
from xknxmono.models.files.v11.split_infos_t import SplitInfos
from xknxmono.models.files.v11.topology_t import Topology
from xknxmono.models.files.v11.trades_t import Trades

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ProjectInstallationsInstallation:
    class Meta:
        global_type = False

    topology: Topology = field(
        metadata={
            "name": "Topology",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        }
    )
    buildings: Locations = field(
        metadata={
            "name": "Buildings",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        }
    )
    group_addresses: GroupAddresses = field(
        metadata={
            "name": "GroupAddresses",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        }
    )
    trades: None | Trades = field(
        default=None,
        metadata={
            "name": "Trades",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        },
    )
    bus_access: None | BusAccess = field(
        default=None,
        metadata={
            "name": "BusAccess",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        },
    )
    split_infos: None | SplitInfos = field(
        default=None,
        metadata={
            "name": "SplitInfos",
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
    installation_id: None | int = field(
        default=None,
        metadata={
            "name": "InstallationId",
            "type": "Attribute",
            "max_inclusive": 15,
        },
    )
    bcukey: int = field(
        default=4294967295,
        metadata={
            "name": "BCUKey",
            "type": "Attribute",
        },
    )
    iprouting_multicast_address: str = field(
        default="224.0.23.12",
        metadata={
            "name": "IPRoutingMulticastAddress",
            "type": "Attribute",
            "pattern": r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    default_line: None | str = field(
        default=None,
        metadata={
            "name": "DefaultLine",
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
    split_type: None | ProjectInstallationsInstallationSplitType = field(
        default=None,
        metadata={
            "name": "SplitType",
            "type": "Attribute",
        },
    )
