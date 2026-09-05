from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/11"


class ToDoStatus(Enum):
    OPEN = "Open"
    ACCOMPLISHED = "Accomplished"
