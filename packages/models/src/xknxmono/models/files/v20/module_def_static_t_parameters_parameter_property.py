from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.property_parameter_t import PropertyParameter

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParametersParameterProperty(PropertyParameter):
    """
    :ivar base_offset: registration-relevant
    :ivar base_index: registration-relevant
    :ivar base_occurrence: registration-relevant
    """

    class Meta:
        global_type = False

    base_offset: None | str = field(
        default=None,
        metadata={
            "name": "BaseOffset",
            "type": "Attribute",
        },
    )
    base_index: None | str = field(
        default=None,
        metadata={
            "name": "BaseIndex",
            "type": "Attribute",
        },
    )
    base_occurrence: None | str = field(
        default=None,
        metadata={
            "name": "BaseOccurrence",
            "type": "Attribute",
        },
    )
