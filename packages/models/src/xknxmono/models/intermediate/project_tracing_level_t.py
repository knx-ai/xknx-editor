from __future__ import annotations
from enum import Enum


class ProjectTracingLevel(Enum):
    NONE = "None"
    OPERATION_USED = "OperationUsed"
    DETAILED = "Detailed"
