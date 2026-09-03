from __future__ import annotations

from enum import Enum


class RftxCapabilities(Enum):
    READY = "Ready"
    READY_FAST = "ReadyFast"
    READY_FAST_SLOW = "ReadyFastSlow"
