from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/23"


class ProjectTracingLevel(Enum):
    NONE = "None"
    OPERATION_USED = "OperationUsed"
    DETAILED = "Detailed"
