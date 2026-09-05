from __future__ import annotations
from enum import Enum


class RfrxCapabilities(Enum):
    READY = "Ready"
    READY_FAST = "ReadyFast"
    SLOW = "Slow"
