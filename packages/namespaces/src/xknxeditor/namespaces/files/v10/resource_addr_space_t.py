from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/10"


class ResourceAddrSpace(Enum):
    NONE = "None"
    STANDARD_MEMORY = "StandardMemory"
    USER_MEMORY = "UserMemory"
    SYSTEM_PROPERTY = "SystemProperty"
    APP_PROPERTY = "AppProperty"
    LC_SLAVE_MEMORY = "LcSlaveMemory"
    LC_FILTER_MEMORY = "LcFilterMemory"
    ADC = "ADC"
    CONSTANT = "Constant"
    POINTER = "Pointer"
    PROPERTY = "Property"
    RELATIVE_MEMORY = "RelativeMemory"
