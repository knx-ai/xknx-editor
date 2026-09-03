from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/13"


class MaskVersionManagementModel(Enum):
    NONE = "None"
    BCU1 = "Bcu1"
    BIM_M112 = "BimM112"
    BCU2 = "Bcu2"
    PROPERTY_BASED = "PropertyBased"
    SYSTEM_B = "SystemB"
