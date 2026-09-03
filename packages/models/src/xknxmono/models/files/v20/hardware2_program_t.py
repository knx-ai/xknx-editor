from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.application_program_ref_t import ApplicationProgramRef
from xknxmono.models.files.v20.coupler_capability_t import CouplerCapability
from xknxmono.models.files.v20.registration_info_t import RegistrationInfo

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class Hardware2Program:
    """
    :ivar application_program_ref: registration-relevant list
    :ivar registration_info:
    :ivar id: registration-relevant
    :ivar medium_types:
    :ivar hash:
    :ivar check_sums: registration-relevant
    :ivar loaded_image: registration-relevant
    :ivar coupler_capabilities: registration-relevant
    """

    class Meta:
        name = "Hardware2Program_t"

    application_program_ref: list[ApplicationProgramRef] = field(
        default_factory=list,
        metadata={
            "name": "ApplicationProgramRef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "max_occurs": 2,
        },
    )
    registration_info: None | RegistrationInfo = field(
        default=None,
        metadata={
            "name": "RegistrationInfo",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    medium_types: list[str] = field(
        default_factory=list,
        metadata={
            "name": "MediumTypes",
            "type": "Attribute",
            "tokens": True,
        },
    )
    hash: None | bytes = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    check_sums: None | bytes = field(
        default=None,
        metadata={
            "name": "CheckSums",
            "type": "Attribute",
            "format": "base64",
        },
    )
    loaded_image: None | bytes = field(
        default=None,
        metadata={
            "name": "LoadedImage",
            "type": "Attribute",
            "format": "base64",
        },
    )
    coupler_capabilities: list[CouplerCapability] = field(
        default_factory=list,
        metadata={
            "name": "CouplerCapabilities",
            "type": "Attribute",
            "tokens": True,
        },
    )
