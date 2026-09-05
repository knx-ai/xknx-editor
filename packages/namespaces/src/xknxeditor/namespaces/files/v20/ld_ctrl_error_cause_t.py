from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class LdCtrlErrorCause(Enum):
    RESOURCE_NOT_FOUND = "ResourceNotFound"
    COMPARE_MISMATCH = "CompareMismatch"
