from __future__ import annotations

from enum import Enum


class DownloadBehavior(Enum):
    NONE = "None"
    BACKGROUND = "Background"
    DEFAULT_VALUE = "DefaultValue"
