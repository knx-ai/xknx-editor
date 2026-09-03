from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/21"


class ParameterTypeTypeTimeUihint(Enum):
    TIME_SS = "Time_ss"
    TIME_SSF = "Time_ssf"
    TIME_SSFF = "Time_ssff"
    TIME_SSFFF = "Time_ssfff"
    TIME_MMSS = "Time_mmss"
    TIME_MMSSF = "Time_mmssf"
    TIME_MMSSFF = "Time_mmssff"
    TIME_MMSSFFF = "Time_mmssfff"
    TIME_HHMM = "Time_hhmm"
    TIME_HHMMSS = "Time_hhmmss"
    TIME_HHMMSSF = "Time_hhmmssf"
    TIME_HHMMSSFF = "Time_hhmmssff"
    TIME_HHMMSSFFF = "Time_hhmmssfff"
    TIME_DHH = "Time_dhh"
    TIME_DHHMM = "Time_dhhmm"
    TIME_DHHMMSS = "Time_dhhmmss"
    DURATION_MMSS = "Duration_mmss"
    DURATION_MMSSF = "Duration_mmssf"
    DURATION_MMSSFF = "Duration_mmssff"
    DURATION_MMSSFFF = "Duration_mmssfff"
    DURATION_HHMM = "Duration_hhmm"
    DURATION_HHMMSS = "Duration_hhmmss"
    DURATION_HHMMSSF = "Duration_hhmmssf"
    DURATION_HHMMSSFF = "Duration_hhmmssff"
    DURATION_HHMMSSFFF = "Duration_hhmmssfff"
