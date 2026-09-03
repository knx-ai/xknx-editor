from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.ld_ctrl_compare_base_t import LdCtrlCompareBase
from xknxmono.models.files.v14.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class LdCtrlCompareMem(LdCtrlCompareBase):
    """
    :ivar address_space: registration-relevant
    :ivar address: registration-relevant
    :ivar size: registration-relevant
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
