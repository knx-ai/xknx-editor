from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/14"


class Access(Enum):
    NONE = "None"
    READ = "Read"
    READ_WRITE = "ReadWrite"
