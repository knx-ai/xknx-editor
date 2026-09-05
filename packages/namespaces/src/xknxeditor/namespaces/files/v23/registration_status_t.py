from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/23"


class RegistrationStatus(Enum):
    UNREGISTERED = "Unregistered"
    REGISTERED = "Registered"
    CERTIFIED = "Certified"
    FUTURE_USE_NOT_RECOMMENDED = "FutureUseNotRecommended"
    FUTURE_USE_NOT_ALLOWED = "FutureUseNotAllowed"
