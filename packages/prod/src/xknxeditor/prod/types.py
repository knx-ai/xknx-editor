from __future__ import annotations

from enum import Enum


class ParamTypeKind(Enum):
    ENUM = "enum"
    NUMBER = "number"
    TEXT = "text"
    TIME = "time"
    CHECKBOX = "checkbox"
    PICTURE = "picture"
    UNKNOWN = "unknown"
