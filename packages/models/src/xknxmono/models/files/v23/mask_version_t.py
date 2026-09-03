from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.hawk_configuration_data_t import HawkConfigurationData
from xknxmono.models.files.v23.mask_version_t_downward_compatible_masks import (
    MaskVersionDownwardCompatibleMasks,
)
from xknxmono.models.files.v23.mask_version_t_management_model import (
    MaskVersionManagementModel,
)
from xknxmono.models.files.v23.mask_version_t_mask_entries import MaskVersionMaskEntries

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class MaskVersion:
    class Meta:
        name = "MaskVersion_t"

    downward_compatible_masks: None | MaskVersionDownwardCompatibleMasks = field(
        default=None,
        metadata={
            "name": "DownwardCompatibleMasks",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    mask_entries: None | MaskVersionMaskEntries = field(
        default=None,
        metadata={
            "name": "MaskEntries",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    hawk_configuration_data: list[HawkConfigurationData] = field(
        default_factory=list,
        metadata={
            "name": "HawkConfigurationData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
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
            "max_length": 50,
        }
    )
    mask_version: int = field(
        metadata={
            "name": "MaskVersion",
            "type": "Attribute",
        }
    )
    mgmt_descriptor01: None | bytes = field(
        default=None,
        metadata={
            "name": "MgmtDescriptor01",
            "type": "Attribute",
            "format": "base16",
        },
    )
    management_model: MaskVersionManagementModel = field(
        metadata={
            "name": "ManagementModel",
            "type": "Attribute",
        }
    )
    medium_type_ref_id: str = field(
        metadata={
            "name": "MediumTypeRefId",
            "type": "Attribute",
        }
    )
    other_medium_type_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "OtherMediumTypeRefId",
            "type": "Attribute",
        },
    )
