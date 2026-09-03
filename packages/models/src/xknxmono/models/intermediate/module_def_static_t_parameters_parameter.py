from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.io_tpoint_parameter_t import IoPointParameter
from xknxmono.models.intermediate.module_def_static_t_parameters_parameter_memory import (
    ModuleDefStaticParametersParameterMemory,
)
from xknxmono.models.intermediate.module_def_static_t_parameters_parameter_property import (
    ModuleDefStaticParametersParameterProperty,
)
from xknxmono.models.intermediate.parameter_base_t import ParameterBase


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticParametersParameter(ParameterBase):
    """
    :ivar choice:
    :ivar base_value: registration-relevant
    """

    class Meta:
        global_type = False

    choice: (
        None
        | ModuleDefStaticParametersParameterMemory
        | ModuleDefStaticParametersParameterProperty
        | IoPointParameter
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Memory",
                    "type": ModuleDefStaticParametersParameterMemory,
                },
                {
                    "name": "Property",
                    "type": ModuleDefStaticParametersParameterProperty,
                },
                {
                    "name": "IoTPoint",
                    "type": IoPointParameter,
                },
            ),
        },
    )
    base_value: None | str = field(
        default=None,
        metadata={
            "name": "BaseValue",
            "type": "Attribute",
        },
    )
