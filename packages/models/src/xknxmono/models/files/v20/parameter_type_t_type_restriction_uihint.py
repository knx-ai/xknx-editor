from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class ParameterTypeTypeRestrictionUihint(Enum):
    TEXT = "Text"
    DROP_DOWN = "DropDown"
    BUTTONS = "Buttons"
    SEGMENTED = "Segmented"
