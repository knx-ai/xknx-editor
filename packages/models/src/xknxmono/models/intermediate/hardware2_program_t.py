from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_ref_t import ApplicationProgramRef
from xknxmono.models.intermediate.coupler_capability_t import CouplerCapability
from xknxmono.models.intermediate.registration_info_t import RegistrationInfo
from xknxmono.models.intermediate.rfrx_capabilities_t import RfrxCapabilities
from xknxmono.models.intermediate.rftx_capabilities_t import RftxCapabilities


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
    :ivar rfrx_capabilities: registration-relevant
    :ivar rftx_capabilities: registration-relevant
    :ivar semantics:
    :ivar sleep_cycle_time_seconds: registration-relevant
    """

    class Meta:
        name = "Hardware2Program_t"

    application_program_ref: list[ApplicationProgramRef] = field(
        default_factory=list,
        metadata={
            "name": "ApplicationProgramRef",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    registration_info: None | RegistrationInfo = field(
        default=None,
        metadata={
            "name": "RegistrationInfo",
            "type": "Element",
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
    rfrx_capabilities: None | RfrxCapabilities = field(
        default=None,
        metadata={
            "name": "RFRxCapabilities",
            "type": "Attribute",
        },
    )
    rftx_capabilities: None | RftxCapabilities = field(
        default=None,
        metadata={
            "name": "RFTxCapabilities",
            "type": "Attribute",
        },
    )
    semantics: None | str = field(
        default=None,
        metadata={
            "name": "Semantics",
            "type": "Attribute",
        },
    )
    sleep_cycle_time_seconds: None | int = field(
        default=None,
        metadata={
            "name": "SleepCycleTimeSeconds",
            "type": "Attribute",
        },
    )
