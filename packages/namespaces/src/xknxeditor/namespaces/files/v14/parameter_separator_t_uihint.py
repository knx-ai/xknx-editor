from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/14"


class ParameterSeparatorUihint(Enum):
    HORIZONTAL_RULER = "HorizontalRuler"
    HEADLINE = "Headline"
    INFORMATION = "Information"
    ERROR = "Error"
