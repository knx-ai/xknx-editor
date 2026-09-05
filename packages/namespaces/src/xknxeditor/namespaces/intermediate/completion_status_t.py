from __future__ import annotations

from enum import Enum


class CompletionStatus(Enum):
    UNDEFINED = "Undefined"
    EDITING = "Editing"
    FINISHED_DESIGN = "FinishedDesign"
    FINISHED_COMMISSIONING = "FinishedCommissioning"
    TESTED = "Tested"
    ACCEPTED = "Accepted"
    LOCKED = "Locked"
