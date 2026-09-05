from __future__ import annotations

from enum import Enum


class ComObjectSecurityRequirements(Enum):
    NONE = "None"
    AUTH = "Auth"
    AUTH_AND_CONF = "AuthAndConf"
