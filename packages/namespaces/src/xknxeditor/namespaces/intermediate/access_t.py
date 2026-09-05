from __future__ import annotations

from enum import Enum


class Access(Enum):
    NONE = "None"
    READ = "Read"
    READ_WRITE = "ReadWrite"
