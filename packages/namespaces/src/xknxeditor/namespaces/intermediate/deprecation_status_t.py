from __future__ import annotations

from enum import Enum


class DeprecationStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
