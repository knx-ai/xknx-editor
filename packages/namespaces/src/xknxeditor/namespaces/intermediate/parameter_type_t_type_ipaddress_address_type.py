from __future__ import annotations
from enum import Enum


class ParameterTypeTypeIpaddressAddressType(Enum):
    HOST_ADDRESS = "HostAddress"
    GATEWAY_ADDRESS = "GatewayAddress"
    UNICAST_ADDRESS = "UnicastAddress"
    BROADCAST_ADDRESS = "BroadcastAddress"
    MULTICAST_ADDRESS = "MulticastAddress"
    SUBNET_MASK = "SubnetMask"
