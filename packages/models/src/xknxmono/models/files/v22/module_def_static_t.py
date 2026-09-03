from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.module_def_load_procedures_t import (
    ModuleDefLoadProcedures,
)
from xknxmono.models.files.v22.module_def_static_t_allocators import (
    ModuleDefStaticAllocators,
)
from xknxmono.models.files.v22.module_def_static_t_com_object_refs import (
    ModuleDefStaticComObjectRefs,
)
from xknxmono.models.files.v22.module_def_static_t_com_objects import (
    ModuleDefStaticComObjects,
)
from xknxmono.models.files.v22.module_def_static_t_parameter_calculations import (
    ModuleDefStaticParameterCalculations,
)
from xknxmono.models.files.v22.module_def_static_t_parameter_refs import (
    ModuleDefStaticParameterRefs,
)
from xknxmono.models.files.v22.module_def_static_t_parameter_validations import (
    ModuleDefStaticParameterValidations,
)
from xknxmono.models.files.v22.module_def_static_t_parameters import (
    ModuleDefStaticParameters,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ModuleDefStatic:
    """
    :ivar parameters:
    :ivar parameter_refs:
    :ivar parameter_calculations:
    :ivar parameter_validations:
    :ivar com_objects:
    :ivar com_object_refs:
    :ivar load_procedures:
    :ivar allocators: registration-relevant set
    """

    class Meta:
        name = "ModuleDefStatic_t"

    parameters: None | ModuleDefStaticParameters = field(
        default=None,
        metadata={
            "name": "Parameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    parameter_refs: None | ModuleDefStaticParameterRefs = field(
        default=None,
        metadata={
            "name": "ParameterRefs",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    parameter_calculations: None | ModuleDefStaticParameterCalculations = field(
        default=None,
        metadata={
            "name": "ParameterCalculations",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    parameter_validations: None | ModuleDefStaticParameterValidations = field(
        default=None,
        metadata={
            "name": "ParameterValidations",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    com_objects: None | ModuleDefStaticComObjects = field(
        default=None,
        metadata={
            "name": "ComObjects",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    com_object_refs: None | ModuleDefStaticComObjectRefs = field(
        default=None,
        metadata={
            "name": "ComObjectRefs",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    load_procedures: None | ModuleDefLoadProcedures = field(
        default=None,
        metadata={
            "name": "LoadProcedures",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    allocators: None | ModuleDefStaticAllocators = field(
        default=None,
        metadata={
            "name": "Allocators",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
