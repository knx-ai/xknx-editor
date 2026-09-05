from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/10"


class ParameterTypeTypeTimeUnit(Enum):
    HOURS = "Hours"
    MINUTES = "Minutes"
    SECONDS = "Seconds"
    HUNDRED_MILLISECONDS = "HundredMilliseconds"
    TEN_MILLISECONDS = "TenMilliseconds"
    MILLISECONDS = "Milliseconds"
