from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/13"


class ProcedureType(Enum):
    LOAD = "Load"
    UNLOAD = "Unload"
