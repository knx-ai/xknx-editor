from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/11"


class Access(Enum):
    NONE = "None"
    READ = "Read"
    READ_WRITE = "ReadWrite"
