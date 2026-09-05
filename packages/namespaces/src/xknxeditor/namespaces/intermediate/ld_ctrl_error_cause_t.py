from __future__ import annotations

from enum import Enum


class LdCtrlErrorCause(Enum):
    RESOURCE_NOT_FOUND = "ResourceNotFound"
    COMPARE_MISMATCH = "CompareMismatch"
