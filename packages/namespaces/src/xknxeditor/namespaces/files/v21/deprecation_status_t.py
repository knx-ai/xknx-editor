from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/21"


class DeprecationStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
