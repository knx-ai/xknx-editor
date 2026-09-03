from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.bus_interface_t_connectors_connector import (
    BusInterfaceConnectorsConnector,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class BusInterfaceConnectors:
    class Meta:
        global_type = False

    connector: list[BusInterfaceConnectorsConnector] = field(
        default_factory=list,
        metadata={
            "name": "Connector",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
