from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

from xknxmono.models.files.v12.completion_status_t import CompletionStatus
from xknxmono.models.files.v12.device_instance_t_additional_addresses import (
    DeviceInstanceAdditionalAddresses,
)
from xknxmono.models.files.v12.device_instance_t_binary_data import (
    DeviceInstanceBinaryData,
)
from xknxmono.models.files.v12.device_instance_t_com_object_instance_refs import (
    DeviceInstanceComObjectInstanceRefs,
)
from xknxmono.models.files.v12.device_instance_t_parameter_instance_refs import (
    DeviceInstanceParameterInstanceRefs,
)
from xknxmono.models.files.v12.ipconfig_t import Ipconfig

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class DeviceInstance:
    class Meta:
        name = "DeviceInstance_t"

    parameter_instance_refs: None | DeviceInstanceParameterInstanceRefs = field(
        default=None,
        metadata={
            "name": "ParameterInstanceRefs",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    com_object_instance_refs: None | DeviceInstanceComObjectInstanceRefs = field(
        default=None,
        metadata={
            "name": "ComObjectInstanceRefs",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    additional_addresses: None | DeviceInstanceAdditionalAddresses = field(
        default=None,
        metadata={
            "name": "AdditionalAddresses",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    binary_data: None | DeviceInstanceBinaryData = field(
        default=None,
        metadata={
            "name": "BinaryData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    ipconfig: None | Ipconfig = field(
        default=None,
        metadata={
            "name": "IPConfig",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    product_ref_id: str = field(
        metadata={
            "name": "ProductRefId",
            "type": "Attribute",
        }
    )
    hardware2_program_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "Hardware2ProgramRefId",
            "type": "Attribute",
        },
    )
    address: None | int = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 255,
        },
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    last_modified: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "LastModified",
            "type": "Attribute",
        },
    )
    last_download: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "LastDownload",
            "type": "Attribute",
        },
    )
    last_used_apdulength: None | int = field(
        default=None,
        metadata={
            "name": "LastUsedAPDULength",
            "type": "Attribute",
        },
    )
    read_max_apdulength: None | int = field(
        default=None,
        metadata={
            "name": "ReadMaxAPDULength",
            "type": "Attribute",
        },
    )
    read_max_routing_apdulength: None | int = field(
        default=None,
        metadata={
            "name": "ReadMaxRoutingAPDULength",
            "type": "Attribute",
        },
    )
    installation_hints: None | str = field(
        default=None,
        metadata={
            "name": "InstallationHints",
            "type": "Attribute",
        },
    )
    completion_status: CompletionStatus = field(
        default=CompletionStatus.UNDEFINED,
        metadata={
            "name": "CompletionStatus",
            "type": "Attribute",
        },
    )
    individual_address_loaded: bool = field(
        default=False,
        metadata={
            "name": "IndividualAddressLoaded",
            "type": "Attribute",
        },
    )
    application_program_loaded: bool = field(
        default=False,
        metadata={
            "name": "ApplicationProgramLoaded",
            "type": "Attribute",
        },
    )
    parameters_loaded: bool = field(
        default=False,
        metadata={
            "name": "ParametersLoaded",
            "type": "Attribute",
        },
    )
    communication_part_loaded: bool = field(
        default=False,
        metadata={
            "name": "CommunicationPartLoaded",
            "type": "Attribute",
        },
    )
    medium_config_loaded: bool = field(
        default=False,
        metadata={
            "name": "MediumConfigLoaded",
            "type": "Attribute",
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
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
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
    is_communication_object_visibility_calculated: None | bool = field(
        default=None,
        metadata={
            "name": "IsCommunicationObjectVisibilityCalculated",
            "type": "Attribute",
        },
    )
    broken: bool = field(
        default=False,
        metadata={
            "name": "Broken",
            "type": "Attribute",
        },
    )
    serial_number: None | bytes = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Attribute",
            "format": "base64",
        },
    )
    unique_id: None | str = field(
        default=None,
        metadata={
            "name": "UniqueId",
            "type": "Attribute",
            "pattern": r"\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}",
        },
    )
    is_rfretransmitter: bool = field(
        default=False,
        metadata={
            "name": "IsRFRetransmitter",
            "type": "Attribute",
        },
    )
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
