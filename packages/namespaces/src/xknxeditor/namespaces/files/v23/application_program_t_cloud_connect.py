from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/23"


class ApplicationProgramCloudConnect(Enum):
    PEER = "Peer"
    BROKER = "Broker"
