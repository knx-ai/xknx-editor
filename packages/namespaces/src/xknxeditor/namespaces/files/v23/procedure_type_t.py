from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/23"


class ProcedureType(Enum):
    LOAD = "Load"
    UNLOAD = "Unload"
