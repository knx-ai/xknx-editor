from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.ld_ctrl_base_t import LdCtrlBase
from xknxmono.models.files.v10.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class LdCtrlLoadImageMem(LdCtrlBase):
    """
    :ivar address_space: registration-relevant
    :ivar address: registration-relevant
    :ivar size: registration-relevant
    """

    class Meta:
        name = "LdCtrlLoadImageMem_t"

    address_space: LdCtrlMemAddrSpace = field(
        default=LdCtrlMemAddrSpace.STANDARD,
        metadata={
            "name": "AddressSpace",
            "type": "Attribute",
        },
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
        }
    )
    size: int = field(
        metadata={
            "name": "Size",
            "type": "Attribute",
        }
    )
