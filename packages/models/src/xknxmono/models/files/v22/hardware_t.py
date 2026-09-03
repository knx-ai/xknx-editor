from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.hardware_t_hardware2_programs import (
    HardwareHardware2Programs,
)
from xknxmono.models.files.v22.hardware_t_products import HardwareProducts

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class Hardware:
    """
    :ivar products:
    :ivar hardware2_programs:
    :ivar id: registration-relevant
    :ivar name:
    :ivar serial_number: registration-relevant
    :ivar version_number: registration-relevant
    :ivar bus_current:
    :ivar tp256:
    :ivar is_accessory: registration-relevant
    :ivar has_individual_address: registration-relevant
    :ivar has_application_program: registration-relevant
    :ivar has_application_program2: registration-relevant
    :ivar is_power_supply: registration-relevant
    :ivar is_choke: registration-relevant
    :ivar is_coupler: registration-relevant
    :ivar is_power_line_repeater: registration-relevant
    :ivar is_power_line_signal_filter: registration-relevant
    :ivar is_cable: registration-relevant
    :ivar is_ipenabled: registration-relevant
    :ivar is_rfretransmitter: registration-relevant
    :ivar original_manufacturer: registration-relevant
    :ivar no_download_without_plugin:
    :ivar non_reg_relevant_data_version:
    :ivar internal_description:
    :ivar semantics:
    """

    class Meta:
        name = "Hardware_t"

    products: None | HardwareProducts = field(
        default=None,
        metadata={
            "name": "Products",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    hardware2_programs: None | HardwareHardware2Programs = field(
        default=None,
        metadata={
            "name": "Hardware2Programs",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    serial_number: str = field(
        metadata={
            "name": "SerialNumber",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    version_number: int = field(
        metadata={
            "name": "VersionNumber",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 32767,
        }
    )
    bus_current: None | float = field(
        default=None,
        metadata={
            "name": "BusCurrent",
            "type": "Attribute",
        },
    )
    tp256: None | bool = field(
        default=None,
        metadata={
            "name": "Tp256",
            "type": "Attribute",
        },
    )
    is_accessory: bool = field(
        default=False,
        metadata={
            "name": "IsAccessory",
            "type": "Attribute",
        },
    )
    has_individual_address: bool = field(
        metadata={
            "name": "HasIndividualAddress",
            "type": "Attribute",
        }
    )
    has_application_program: bool = field(
        metadata={
            "name": "HasApplicationProgram",
            "type": "Attribute",
        }
    )
    has_application_program2: bool = field(
        default=False,
        metadata={
            "name": "HasApplicationProgram2",
            "type": "Attribute",
        },
    )
    is_power_supply: bool = field(
        default=False,
        metadata={
            "name": "IsPowerSupply",
            "type": "Attribute",
        },
    )
    is_choke: bool = field(
        default=False,
        metadata={
            "name": "IsChoke",
            "type": "Attribute",
        },
    )
    is_coupler: bool = field(
        default=False,
        metadata={
            "name": "IsCoupler",
            "type": "Attribute",
        },
    )
    is_power_line_repeater: bool = field(
        default=False,
        metadata={
            "name": "IsPowerLineRepeater",
            "type": "Attribute",
        },
    )
    is_power_line_signal_filter: bool = field(
        default=False,
        metadata={
            "name": "IsPowerLineSignalFilter",
            "type": "Attribute",
        },
    )
    is_cable: bool = field(
        default=False,
        metadata={
            "name": "IsCable",
            "type": "Attribute",
        },
    )
    is_ipenabled: bool = field(
        default=False,
        metadata={
            "name": "IsIPEnabled",
            "type": "Attribute",
        },
    )
    is_rfretransmitter: bool = field(
        default=False,
        metadata={
            "name": "IsRFRetransmitter",
            "type": "Attribute",
        },
    )
    original_manufacturer: None | str = field(
        default=None,
        metadata={
            "name": "OriginalManufacturer",
            "type": "Attribute",
        },
    )
    no_download_without_plugin: bool = field(
        default=False,
        metadata={
            "name": "NoDownloadWithoutPlugin",
            "type": "Attribute",
        },
    )
    non_reg_relevant_data_version: int = field(
        default=0,
        metadata={
            "name": "NonRegRelevantDataVersion",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
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
