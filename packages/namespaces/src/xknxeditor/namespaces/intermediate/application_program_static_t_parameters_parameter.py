from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.intermediate.io_tpoint_parameter_t import IoPointParameter
from xknxeditor.namespaces.intermediate.memory_parameter_t import MemoryParameter
from xknxeditor.namespaces.intermediate.parameter_base_t import ParameterBase
from xknxeditor.namespaces.intermediate.property_parameter_t import PropertyParameter


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
                },
                {
                    "name": "Property",
                    "type": PropertyParameter,
                },
                {
                    "name": "IoTPoint",
                    "type": IoPointParameter,
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
