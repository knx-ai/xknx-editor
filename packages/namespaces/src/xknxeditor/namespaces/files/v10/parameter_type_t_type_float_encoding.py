from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/10"


class ParameterTypeTypeFloatEncoding(Enum):
    DPT_9 = "DPT 9"
    IEEE_754_SINGLE = "IEEE-754 Single"
    IEEE_754_DOUBLE = "IEEE-754 Double"
