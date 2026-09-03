from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/11"


class ParameterTypeTypeTimeUnit(Enum):
    HOURS = "Hours"
    MINUTES = "Minutes"
    SECONDS = "Seconds"
    HUNDRED_MILLISECONDS = "HundredMilliseconds"
    TEN_MILLISECONDS = "TenMilliseconds"
    MILLISECONDS = "Milliseconds"
    PACKED_SECONDS_AND_MILLISECONDS = "PackedSecondsAndMilliseconds"
    PACKED_DAYS_HOURS_MINUTES_AND_SECONDS = "PackedDaysHoursMinutesAndSeconds"
