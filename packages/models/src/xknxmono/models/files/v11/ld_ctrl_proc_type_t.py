from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/11"


class LdCtrlProcType(Enum):
    FULL = "full"
    PAR = "par"
    GRP = "grp"
    FULL_PAR = "full,par"
    FULL_GRP = "full,grp"
    PAR_GRP = "par,grp"
    ALL = "all"
    AUTO = "auto"
