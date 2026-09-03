from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_address_table import (
    ApplicationProgramStaticAddressTable,
)
from xknxmono.models.intermediate.application_program_static_t_allocators import (
    ApplicationProgramStaticAllocators,
)
from xknxmono.models.intermediate.application_program_static_t_association_table import (
    ApplicationProgramStaticAssociationTable,
)
from xknxmono.models.intermediate.application_program_static_t_binary_data import (
    ApplicationProgramStaticBinaryData,
)
from xknxmono.models.intermediate.application_program_static_t_bus_interfaces import (
    ApplicationProgramStaticBusInterfaces,
)
from xknxmono.models.intermediate.application_program_static_t_code import (
    ApplicationProgramStaticCode,
)
from xknxmono.models.intermediate.application_program_static_t_com_object_refs import (
    ApplicationProgramStaticComObjectRefs,
)
from xknxmono.models.intermediate.application_program_static_t_com_object_table import (
    ApplicationProgramStaticComObjectTable,
)
from xknxmono.models.intermediate.application_program_static_t_device_compare import (
    ApplicationProgramStaticDeviceCompare,
)
from xknxmono.models.intermediate.application_program_static_t_extension import (
    ApplicationProgramStaticExtension,
)
from xknxmono.models.intermediate.application_program_static_t_fixup_list import (
    ApplicationProgramStaticFixupList,
)
from xknxmono.models.intermediate.application_program_static_t_messages import (
    ApplicationProgramStaticMessages,
)
from xknxmono.models.intermediate.application_program_static_t_options import (
    ApplicationProgramStaticOptions,
)
from xknxmono.models.intermediate.application_program_static_t_parameter_calculations import (
    ApplicationProgramStaticParameterCalculations,
)
from xknxmono.models.intermediate.application_program_static_t_parameter_refs import (
    ApplicationProgramStaticParameterRefs,
)
from xknxmono.models.intermediate.application_program_static_t_parameter_types import (
    ApplicationProgramStaticParameterTypes,
)
from xknxmono.models.intermediate.application_program_static_t_parameter_validations import (
    ApplicationProgramStaticParameterValidations,
)
from xknxmono.models.intermediate.application_program_static_t_parameters import (
    ApplicationProgramStaticParameters,
)
from xknxmono.models.intermediate.application_program_static_t_script import (
    ApplicationProgramStaticScript,
)
from xknxmono.models.intermediate.application_program_static_t_security_roles import (
    ApplicationProgramStaticSecurityRoles,
)
from xknxmono.models.intermediate.load_procedures_t import LoadProcedures


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStatic:
    """
    :ivar code:
    :ivar parameter_types:
    :ivar parameters:
    :ivar parameter_refs:
    :ivar parameter_calculations:
    :ivar parameter_validations:
    :ivar com_object_table:
    :ivar com_object_refs:
    :ivar address_table:
    :ivar association_table:
    :ivar fixup_list:
    :ivar load_procedures:
    :ivar extension:
    :ivar binary_data:
    :ivar device_compare:
    :ivar messages:
    :ivar script: registration-relevant
    :ivar security_roles: registration-relevant set
    :ivar bus_interfaces: registration-relevant set
    :ivar allocators: registration-relevant set
    :ivar options:
    """

    class Meta:
        name = "ApplicationProgramStatic_t"

    code: None | ApplicationProgramStaticCode = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
        },
    )
    parameter_types: None | ApplicationProgramStaticParameterTypes = field(
        default=None,
        metadata={
            "name": "ParameterTypes",
            "type": "Element",
        },
    )
    parameters: None | ApplicationProgramStaticParameters = field(
        default=None,
        metadata={
            "name": "Parameters",
            "type": "Element",
        },
    )
    parameter_refs: None | ApplicationProgramStaticParameterRefs = field(
        default=None,
        metadata={
            "name": "ParameterRefs",
            "type": "Element",
        },
    )
    parameter_calculations: None | ApplicationProgramStaticParameterCalculations = (
        field(
            default=None,
            metadata={
                "name": "ParameterCalculations",
                "type": "Element",
            },
        )
    )
    parameter_validations: None | ApplicationProgramStaticParameterValidations = field(
        default=None,
        metadata={
            "name": "ParameterValidations",
            "type": "Element",
        },
    )
    com_object_table: None | ApplicationProgramStaticComObjectTable = field(
        default=None,
        metadata={
            "name": "ComObjectTable",
            "type": "Element",
        },
    )
    com_object_refs: None | ApplicationProgramStaticComObjectRefs = field(
        default=None,
        metadata={
            "name": "ComObjectRefs",
            "type": "Element",
        },
    )
    address_table: None | ApplicationProgramStaticAddressTable = field(
        default=None,
        metadata={
            "name": "AddressTable",
            "type": "Element",
        },
    )
    association_table: None | ApplicationProgramStaticAssociationTable = field(
        default=None,
        metadata={
            "name": "AssociationTable",
            "type": "Element",
        },
    )
    fixup_list: None | ApplicationProgramStaticFixupList = field(
        default=None,
        metadata={
            "name": "FixupList",
            "type": "Element",
        },
    )
    load_procedures: None | LoadProcedures = field(
        default=None,
        metadata={
            "name": "LoadProcedures",
            "type": "Element",
        },
    )
    extension: None | ApplicationProgramStaticExtension = field(
        default=None,
        metadata={
            "name": "Extension",
            "type": "Element",
        },
    )
    binary_data: None | ApplicationProgramStaticBinaryData = field(
        default=None,
        metadata={
            "name": "BinaryData",
            "type": "Element",
        },
    )
    device_compare: None | ApplicationProgramStaticDeviceCompare = field(
        default=None,
        metadata={
            "name": "DeviceCompare",
            "type": "Element",
        },
    )
    messages: None | ApplicationProgramStaticMessages = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
        },
    )
    script: None | ApplicationProgramStaticScript = field(
        default=None,
        metadata={
            "name": "Script",
            "type": "Element",
        },
    )
    security_roles: None | ApplicationProgramStaticSecurityRoles = field(
        default=None,
        metadata={
            "name": "SecurityRoles",
            "type": "Element",
        },
    )
    bus_interfaces: None | ApplicationProgramStaticBusInterfaces = field(
        default=None,
        metadata={
            "name": "BusInterfaces",
            "type": "Element",
        },
    )
    allocators: None | ApplicationProgramStaticAllocators = field(
        default=None,
        metadata={
            "name": "Allocators",
            "type": "Element",
        },
    )
    options: None | ApplicationProgramStaticOptions = field(
        default=None,
        metadata={
            "name": "Options",
            "type": "Element",
        },
    )
