from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/10"


class ComObjectPriority(Enum):
    LOW = "Low"
    HIGH = "High"
    ALERT = "Alert"
