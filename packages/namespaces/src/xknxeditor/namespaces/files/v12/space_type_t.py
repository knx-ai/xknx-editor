from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/12"


class SpaceType(Enum):
    BUILDING = "Building"
    BUILDING_PART = "BuildingPart"
    FLOOR = "Floor"
    ROOM = "Room"
    DISTRIBUTION_BOARD = "DistributionBoard"
    STAIRWAY = "Stairway"
    CORRIDOR = "Corridor"
