from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/21"


class NodeType(Enum):
    FOLDER = "Folder"
    CHANNEL = "Channel"
