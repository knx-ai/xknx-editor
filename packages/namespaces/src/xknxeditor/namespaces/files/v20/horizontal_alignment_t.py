from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class HorizontalAlignment(Enum):
    LEFT = "Left"
    MIDDLE = "Middle"
    RIGHT = "Right"
    STRETCH = "Stretch"
    REPEAT = "Repeat"
