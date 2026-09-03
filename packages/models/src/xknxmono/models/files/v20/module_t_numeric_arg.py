from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.module_arg_t import ModuleArg

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ModuleNumericArg(ModuleArg):
    """
    :ivar value: registration-relevant
    :ivar allocator_ref_id: registration-relevant
    :ivar base_value: registration-relevant
    """

    class Meta:
        global_type = False

    value: None | int = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        },
    )
    allocator_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "AllocatorRefId",
            "type": "Attribute",
        },
    )
    base_value: None | str = field(
        default=None,
        metadata={
            "name": "BaseValue",
            "type": "Attribute",
        },
    )
