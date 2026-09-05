from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/21"


class LdCtrlControlVariable(Enum):
    ENABLE_SEGMENT_WRITE = "EnableSegmentWrite"
    ENABLE_VERIFY_ON_WRITE_DIRECT = "EnableVerifyOnWriteDirect"
    ENABLE_OPTIMISTIC_WRITE = "EnableOptimisticWrite"
    ENABLE_MEMORY_AUTO_VERIFY = "EnableMemoryAutoVerify"
