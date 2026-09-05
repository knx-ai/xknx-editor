from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/10"


class ParameterTypeTypeNumberType(Enum):
    SIGNED_INT = "signedInt"
    UNSIGNED_INT = "unsignedInt"
