from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.ld_ctrl_base_t import LdCtrlBase
from xknxmono.models.files.v12.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class LdCtrlWriteMem(LdCtrlBase):
    """
    :ivar address_space: registration-relevant
    :ivar address: registration-relevant
    :ivar size: registration-relevant
    :ivar verify: registration-relevant
    :ivar inline_data: registration-relevant
    """

    class Meta:
        name = "LdCtrlWriteMem_t"

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
    verify: bool = field(
        metadata={
            "name": "Verify",
            "type": "Attribute",
        }
    )
    inline_data: None | bytes = field(
        default=None,
        metadata={
            "name": "InlineData",
            "type": "Attribute",
            "format": "base16",
        },
    )
