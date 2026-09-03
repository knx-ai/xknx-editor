from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.prop_type_t import PropType

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty:
    class Meta:
        global_type = False

    property_id: int = field(
        metadata={
            "name": "PropertyID",
            "type": "Attribute",
        }
    )
    property_data_type: None | PropType = field(
        default=None,
        metadata={
            "name": "PropertyDataType",
            "type": "Attribute",
        },
    )
