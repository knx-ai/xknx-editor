from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/12"


class ParameterTypeTypeIpaddressAddressType(Enum):
    HOST_ADDRESS = "HostAddress"
    GATEWAY_ADDRESS = "GatewayAddress"
    UNICAST_ADDRESS = "UnicastAddress"
    BROADCAST_ADDRESS = "BroadcastAddress"
    MULTICAST_ADDRESS = "MulticastAddress"
    SUBNET_MASK = "SubnetMask"
