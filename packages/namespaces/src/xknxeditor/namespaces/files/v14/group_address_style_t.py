from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/14"


class GroupAddressStyle(Enum):
    TWO_LEVEL = "TwoLevel"
    THREE_LEVEL = "ThreeLevel"
    FREE = "Free"
