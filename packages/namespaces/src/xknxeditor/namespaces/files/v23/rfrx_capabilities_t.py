from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/23"


class RfrxCapabilities(Enum):
    READY = "Ready"
    READY_FAST = "ReadyFast"
    SLOW = "Slow"
