from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDate

from xknxmono.models.files.v21.registration_info_t_registration_key import (
    RegistrationInfoRegistrationKey,
)
from xknxmono.models.files.v21.registration_status_t import RegistrationStatus

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class RegistrationInfo:
    """
    :ivar registration_status: registration-relevant
    :ivar registration_number: registration-relevant
    :ivar original_registration_number: registration-relevant
    :ivar registration_date: registration-relevant
    :ivar registration_signature: registration-relevant
    :ivar registration_key: registration-relevant
    """

    class Meta:
        name = "RegistrationInfo_t"

    registration_status: RegistrationStatus = field(
        metadata={
            "name": "RegistrationStatus",
            "type": "Attribute",
        }
    )
    registration_number: None | str = field(
        default=None,
        metadata={
            "name": "RegistrationNumber",
            "type": "Attribute",
            "pattern": r"\d{4}/\d+",
        },
    )
    original_registration_number: None | str = field(
        default=None,
        metadata={
            "name": "OriginalRegistrationNumber",
            "type": "Attribute",
            "pattern": r"\d{4}/\d+",
        },
    )
    registration_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RegistrationDate",
            "type": "Attribute",
        },
    )
    registration_signature: None | bytes = field(
        default=None,
        metadata={
            "name": "RegistrationSignature",
            "type": "Attribute",
            "format": "base64",
        },
    )
    registration_key: RegistrationInfoRegistrationKey = field(
        default=RegistrationInfoRegistrationKey.KNXCONV,
        metadata={
            "name": "RegistrationKey",
            "type": "Attribute",
        },
    )
