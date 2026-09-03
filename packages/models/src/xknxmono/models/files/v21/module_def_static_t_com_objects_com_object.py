from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.com_object_t import ComObject

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticComObjectsComObject(ComObject):
    """
    :ivar base_number: registration-relevant
    """

    class Meta:
        global_type = False

    base_number: None | str = field(
        default=None,
        metadata={
            "name": "BaseNumber",
            "type": "Attribute",
        },
    )
