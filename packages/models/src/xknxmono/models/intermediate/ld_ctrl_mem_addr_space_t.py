from __future__ import annotations

from enum import Enum


class LdCtrlMemAddrSpace(Enum):
    STANDARD = "Standard"
    USER = "User"
    LC_SLAVE = "LcSlave"
    LC_FILTER = "LcFilter"
