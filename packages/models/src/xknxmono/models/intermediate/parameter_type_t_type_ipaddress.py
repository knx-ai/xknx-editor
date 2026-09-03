from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.parameter_type_t_type_ipaddress_address_type import (
    ParameterTypeTypeIpaddressAddressType,
)
from xknxmono.models.intermediate.parameter_type_t_type_ipaddress_version import (
    ParameterTypeTypeIpaddressVersion,
)


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeIpaddress:
    """
    :ivar address_type: registration-relevant
    :ivar version: registration-relevant
    """

    class Meta:
        global_type = False

    address_type: ParameterTypeTypeIpaddressAddressType = field(
        metadata={
            "name": "AddressType",
            "type": "Attribute",
        }
    )
    version: ParameterTypeTypeIpaddressVersion = field(
        default=ParameterTypeTypeIpaddressVersion.IPV4,
        metadata={
            "name": "Version",
            "type": "Attribute",
        },
    )
