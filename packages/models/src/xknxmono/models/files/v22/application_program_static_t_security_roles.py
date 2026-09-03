from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.application_program_static_t_security_roles_security_role import (
    ApplicationProgramStaticSecurityRolesSecurityRole,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticSecurityRoles:
    class Meta:
        global_type = False

    security_role: list[ApplicationProgramStaticSecurityRolesSecurityRole] = field(
        default_factory=list,
        metadata={
            "name": "SecurityRole",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
