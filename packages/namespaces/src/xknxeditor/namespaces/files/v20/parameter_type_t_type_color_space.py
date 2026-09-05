from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class ParameterTypeTypeColorSpace(Enum):
    RGB = "RGB"
    HSV = "HSV"
    RGBW = "RGBW"
