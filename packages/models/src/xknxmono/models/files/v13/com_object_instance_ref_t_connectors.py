from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.com_object_instance_ref_t_connectors_receive import (
    ComObjectInstanceRefConnectorsReceive,
)
from xknxmono.models.files.v13.com_object_instance_ref_t_connectors_send import (
    ComObjectInstanceRefConnectorsSend,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ComObjectInstanceRefConnectors:
    class Meta:
        global_type = False

    send: ComObjectInstanceRefConnectorsSend = field(
        metadata={
            "name": "Send",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        }
    )
    receive: list[ComObjectInstanceRefConnectorsReceive] = field(
        default_factory=list,
        metadata={
            "name": "Receive",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
