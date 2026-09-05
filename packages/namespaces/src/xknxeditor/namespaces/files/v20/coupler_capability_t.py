from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class CouplerCapability(Enum):
    RF_READY = "RfReady"
    RF_MULTI_FAST = "RfMultiFast"
    RF_MULTI_SLOW = "RfMultiSlow"
    SECURITY_PROXY = "SecurityProxy"
