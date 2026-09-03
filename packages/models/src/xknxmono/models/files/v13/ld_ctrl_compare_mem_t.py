from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.ld_ctrl_base_t import LdCtrlBase
from xknxmono.models.files.v13.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class LdCtrlCompareMem(LdCtrlBase):
    """
    :ivar address_space: registration-relevant
    :ivar address: registration-relevant
    :ivar size: registration-relevant
    :ivar inline_data: registration-relevant
    """

    class Meta:
        name = "LdCtrlCompareMem_t"

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
    inline_data: bytes = field(
        metadata={
            "name": "InlineData",
            "type": "Attribute",
            "format": "base16",
        }
    )
