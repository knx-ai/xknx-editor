from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/13"


class DownloadBehavior(Enum):
    NONE = "None"
    BACKGROUND = "Background"
    DEFAULT_VALUE = "DefaultValue"
