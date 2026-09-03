from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.hawk_configuration_data_t_procedures_procedure import (
    HawkConfigurationDataProceduresProcedure,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataProcedures:
    class Meta:
        global_type = False

    procedure: list[HawkConfigurationDataProceduresProcedure] = field(
        default_factory=list,
        metadata={
            "name": "Procedure",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
