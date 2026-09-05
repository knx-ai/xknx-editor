from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/13"


class LdCtrlMemAddrSpace(Enum):
    STANDARD = "Standard"
    USER = "User"
    LC_SLAVE = "LcSlave"
    LC_FILTER = "LcFilter"
