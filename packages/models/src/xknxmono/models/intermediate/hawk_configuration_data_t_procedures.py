from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.hawk_configuration_data_t_procedures_procedure import (
    HawkConfigurationDataProceduresProcedure,
)


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataProcedures:
    class Meta:
        global_type = False

    procedure: list[HawkConfigurationDataProceduresProcedure] = field(
        default_factory=list,
        metadata={
            "name": "Procedure",
            "type": "Element",
            "min_occurs": 1,
        },
    )
