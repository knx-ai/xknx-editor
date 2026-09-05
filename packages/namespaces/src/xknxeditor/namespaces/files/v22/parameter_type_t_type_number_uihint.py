from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/22"


class ParameterTypeTypeNumberUihint(Enum):
    SLIDER = "Slider"
    CHECK_BOX = "CheckBox"
    PROGRESS_BAR = "ProgressBar"
