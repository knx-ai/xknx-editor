from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticSecurityRolesSecurityRole:
    """
    :ivar id: registration-relevant
    :ivar text:
    :ivar mask: registration-relevant
    :ivar role_id:
    """

    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    mask: int = field(
        metadata={
            "name": "Mask",
            "type": "Attribute",
        }
    )
    role_id: None | int = field(
        default=None,
        metadata={
            "name": "RoleID",
            "type": "Attribute",
        },
    )
