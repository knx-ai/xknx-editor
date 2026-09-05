from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.intermediate.bus_interface_t_connectors_connector import (
    BusInterfaceConnectorsConnector,
)


@dataclass(slots=True, kw_only=True)
class BusInterfaceConnectors:
    class Meta:
        global_type = False

    connector: list[BusInterfaceConnectorsConnector] = field(
        default_factory=list,
        metadata={
            "name": "Connector",
            "type": "Element",
        },
    )
