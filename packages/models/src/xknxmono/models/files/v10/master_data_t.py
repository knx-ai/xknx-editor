from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.master_data_t_datapoint_types import (
    MasterDataDatapointTypes,
)
from xknxmono.models.files.v10.master_data_t_languages import MasterDataLanguages
from xknxmono.models.files.v10.master_data_t_manufacturers import (
    MasterDataManufacturers,
)
from xknxmono.models.files.v10.master_data_t_mask_versions import MasterDataMaskVersions
from xknxmono.models.files.v10.master_data_t_medium_types import MasterDataMediumTypes

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class MasterData:
    class Meta:
        name = "MasterData_t"

    datapoint_types: None | MasterDataDatapointTypes = field(
        default=None,
        metadata={
            "name": "DatapointTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    medium_types: None | MasterDataMediumTypes = field(
        default=None,
        metadata={
            "name": "MediumTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    mask_versions: None | MasterDataMaskVersions = field(
        default=None,
        metadata={
            "name": "MaskVersions",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    manufacturers: None | MasterDataManufacturers = field(
        default=None,
        metadata={
            "name": "Manufacturers",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    languages: None | MasterDataLanguages = field(
        default=None,
        metadata={
            "name": "Languages",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    version: int = field(
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )
    signature: bytes = field(
        metadata={
            "name": "Signature",
            "type": "Attribute",
            "format": "base64",
        }
    )
