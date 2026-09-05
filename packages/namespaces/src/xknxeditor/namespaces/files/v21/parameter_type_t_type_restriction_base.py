from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/21"


class ParameterTypeTypeRestrictionBase(Enum):
    VALUE = "Value"
    BINARY_VALUE = "BinaryValue"
