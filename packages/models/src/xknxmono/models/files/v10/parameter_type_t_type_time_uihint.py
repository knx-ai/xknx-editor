from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/10"


class ParameterTypeTypeTimeUihint(Enum):
    TIME_HHMM = "Time_hhmm"
    TIME_HHMMSS = "Time_hhmmss"
    TIME_HHMMSSF = "Time_hhmmssf"
    TIME_HHMMSSFF = "Time_hhmmssff"
    TIME_HHMMSSFFF = "Time_hhmmssfff"
    DURATION_HHMM = "Duration_hhmm"
    DURATION_HHMMSS = "Duration_hhmmss"
    DURATION_HHMMSSF = "Duration_hhmmssf"
    DURATION_HHMMSSFF = "Duration_hhmmssff"
    DURATION_HHMMSSFFF = "Duration_hhmmssfff"
