from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.files.v23.io_tpoint_parameter_t import IoPointParameter
from xknxmono.models.files.v23.memory_parameter_t import MemoryParameter
from xknxmono.models.files.v23.parameter_base_t import ParameterBase
from xknxmono.models.files.v23.property_parameter_t import PropertyParameter

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticParametersParameter(ParameterBase):
    """
    :ivar choice:
    :ivar legacy_patch_always: registration-relevant
    """

    class Meta:
        global_type = False

    choice: None | MemoryParameter | PropertyParameter | IoPointParameter = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Memory",
                    "type": MemoryParameter,
                    "namespace": "http://knx.org/xml/project/23",
                },
                {
                    "name": "Property",
                    "type": PropertyParameter,
                    "namespace": "http://knx.org/xml/project/23",
                },
                {
                    "name": "IoTPoint",
                    "type": IoPointParameter,
                    "namespace": "http://knx.org/xml/project/23",
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
