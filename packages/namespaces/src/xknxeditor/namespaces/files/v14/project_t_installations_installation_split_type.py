from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/14"


class ProjectInstallationsInstallationSplitType(Enum):
    NONE = "None"
    MASTER = "Master"
    SPLIT = "Split"
