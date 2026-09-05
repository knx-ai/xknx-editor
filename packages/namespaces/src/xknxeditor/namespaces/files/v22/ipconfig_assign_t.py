from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/22"


class IpconfigAssign(Enum):
    FIXED = "Fixed"
    AUTO = "Auto"
