from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.module_def_static_t_parameters_parameter_memory import (
    ModuleDefStaticParametersParameterMemory,
)
from xknxmono.models.files.v20.module_def_static_t_parameters_parameter_property import (
    ModuleDefStaticParametersParameterProperty,
)
from xknxmono.models.files.v20.parameter_base_t import ParameterBase

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Memory",
                    "type": ModuleDefStaticParametersParameterMemory,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "Property",
                    "type": ModuleDefStaticParametersParameterProperty,
                    "namespace": "http://knx.org/xml/project/20",
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
