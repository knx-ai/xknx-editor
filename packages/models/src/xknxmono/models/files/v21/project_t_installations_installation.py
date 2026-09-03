from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.completion_status_t import CompletionStatus
from xknxmono.models.files.v21.group_addresses_t import GroupAddresses
from xknxmono.models.files.v21.locations_t import Locations
from xknxmono.models.files.v21.p2_plinks_t import P2Plinks
from xknxmono.models.files.v21.project_t_installations_installation_split_type import (
    ProjectInstallationsInstallationSplitType,
)
from xknxmono.models.files.v21.security_mode_t import SecurityMode
from xknxmono.models.files.v21.split_infos_t import SplitInfos
from xknxmono.models.files.v21.topology_t import Topology
from xknxmono.models.files.v21.trades_t import Trades

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ProjectInstallationsInstallation:
    class Meta:
        global_type = False

    topology: Topology = field(
        metadata={
            "name": "Topology",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        }
    )
    locations: Locations = field(
        metadata={
            "name": "Locations",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        }
    )
    group_addresses: GroupAddresses = field(
        metadata={
            "name": "GroupAddresses",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        }
    )
    p2_plinks: None | P2Plinks = field(
        default=None,
        metadata={
            "name": "P2PLinks",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
    trades: None | Trades = field(
        default=None,
        metadata={
            "name": "Trades",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
    split_infos: None | SplitInfos = field(
        default=None,
        metadata={
            "name": "SplitInfos",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
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
    multicast_ttl: int = field(
        default=16,
        metadata={
            "name": "MulticastTTL",
            "type": "Attribute",
        },
    )
    iprouting_backbone_key: None | str = field(
        default=None,
        metadata={
            "name": "IPRoutingBackboneKey",
            "type": "Attribute",
            "max_length": 100,
        },
    )
    iprouting_latency_tolerance: None | int = field(
        default=None,
        metadata={
            "name": "IPRoutingLatencyTolerance",
            "type": "Attribute",
        },
    )
    ipsync_latency_fraction: float = field(
        default=0.1,
        metadata={
            "name": "IPSyncLatencyFraction",
            "type": "Attribute",
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
    iprouting_backbone_security: SecurityMode = field(
        default=SecurityMode.AUTO,
        metadata={
            "name": "IPRoutingBackboneSecurity",
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
    context: None | str = field(
        default=None,
        metadata={
            "name": "Context",
            "type": "Attribute",
        },
    )
