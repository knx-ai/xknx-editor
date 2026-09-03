from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.memory_parameter_t import MemoryParameter
from xknxmono.models.files.v11.parameter_base_t import ParameterBase
from xknxmono.models.files.v11.property_parameter_t import PropertyParameter

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParametersParameter(ParameterBase):
    """
    :ivar choice:
    :ivar legacy_patch_always: registration-relevant
    """

    class Meta:
        global_type = False

    choice: None | MemoryParameter | PropertyParameter = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Memory",
                    "type": MemoryParameter,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "Property",
                    "type": PropertyParameter,
                    "namespace": "http://knx.org/xml/project/11",
                },
            ),
        },
    )
    legacy_patch_always: bool = field(
        default=False,
        metadata={
            "name": "LegacyPatchAlways",
            "type": "Attribute",
        },
    )
