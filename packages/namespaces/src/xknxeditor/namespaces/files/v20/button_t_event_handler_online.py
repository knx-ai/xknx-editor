from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class ButtonEventHandlerOnline(Enum):
    CONNECTION_LESS = "ConnectionLess"
    CONNECTION_ORIENTED = "ConnectionOriented"
