from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/14"


class ResourceAccessRights(Enum):
    NONE = "None"
    SYSTEM_MANUFACTURER = "SystemManufacturer"
    MANUFACTURER = "Manufacturer"
    CONFIGURATION = "Configuration"
    RUNTIME = "Runtime"
