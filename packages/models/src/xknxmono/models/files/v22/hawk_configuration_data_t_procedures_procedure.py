from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.hawk_configuration_data_t_procedures_procedure_value import (
    HawkConfigurationDataProceduresProcedureValue,
)
from xknxmono.models.files.v22.ld_ctrl_proc_type_t import LdCtrlProcType
from xknxmono.models.files.v22.load_procedure_t import LoadProcedure
from xknxmono.models.files.v22.procedure_type_t import ProcedureType
from xknxmono.models.files.v22.resource_access_t import ResourceAccess

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataProceduresProcedure(LoadProcedure):
    class Meta:
        global_type = False

    procedure_type: ProcedureType = field(
        metadata={
            "name": "ProcedureType",
            "type": "Attribute",
        }
    )
    procedure_sub_type: (
        LdCtrlProcType | HawkConfigurationDataProceduresProcedureValue
    ) = field(
        metadata={
            "name": "ProcedureSubType",
            "type": "Attribute",
        }
    )
    access: list[ResourceAccess] = field(
        default_factory=list,
        metadata={
            "name": "Access",
            "type": "Attribute",
            "tokens": True,
        },
    )
