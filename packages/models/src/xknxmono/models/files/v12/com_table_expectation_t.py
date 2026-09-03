from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/12"


class ComTableExpectation(Enum):
    YES = "Yes"
    NO = "No"
    TRY = "Try"
