from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/12"


class ResourceAccess(Enum):
    REMOTE = "remote"
    LOCAL1 = "local1"
    LOCAL2 = "local2"
