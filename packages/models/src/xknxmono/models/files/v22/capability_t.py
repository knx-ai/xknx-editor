from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/22"


class Capability(Enum):
    ADD_DELETE_DEVICE = "AddDeleteDevice"
    GROUP_COMMUNICATION_EVENTS = "GroupCommunicationEvents"
    GROUP_COMMUNICATION_LIMITS = "GroupCommunicationLimits"
    TRANSFER_PARAMETERS = "TransferParameters"
    PROJECT_CHECK = "ProjectCheck"
    PRINTING = "Printing"
