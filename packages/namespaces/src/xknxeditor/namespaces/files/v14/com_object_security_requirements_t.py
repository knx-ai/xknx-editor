from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/14"


class ComObjectSecurityRequirements(Enum):
    NONE = "None"
    AUTH = "Auth"
    AUTH_AND_CONF = "AuthAndConf"
