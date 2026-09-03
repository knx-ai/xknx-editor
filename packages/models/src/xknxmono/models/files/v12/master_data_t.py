from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.master_data_t_datapoint_types import (
    MasterDataDatapointTypes,
)
from xknxmono.models.files.v12.master_data_t_functional_blocks import (
    MasterDataFunctionalBlocks,
)
from xknxmono.models.files.v12.master_data_t_interface_object_properties import (
    MasterDataInterfaceObjectProperties,
)
from xknxmono.models.files.v12.master_data_t_interface_object_types import (
    MasterDataInterfaceObjectTypes,
)
from xknxmono.models.files.v12.master_data_t_languages import MasterDataLanguages
from xknxmono.models.files.v12.master_data_t_manufacturers import (
    MasterDataManufacturers,
)
from xknxmono.models.files.v12.master_data_t_mask_versions import MasterDataMaskVersions
from xknxmono.models.files.v12.master_data_t_medium_types import MasterDataMediumTypes
from xknxmono.models.files.v12.master_data_t_product_languages import (
    MasterDataProductLanguages,
)
from xknxmono.models.files.v12.master_data_t_property_data_types import (
    MasterDataPropertyDataTypes,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class MasterData:
    class Meta:
        name = "MasterData_t"

    datapoint_types: None | MasterDataDatapointTypes = field(
        default=None,
        metadata={
            "name": "DatapointTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    interface_object_types: None | MasterDataInterfaceObjectTypes = field(
        default=None,
        metadata={
            "name": "InterfaceObjectTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    interface_object_properties: None | MasterDataInterfaceObjectProperties = field(
        default=None,
        metadata={
            "name": "InterfaceObjectProperties",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    property_data_types: None | MasterDataPropertyDataTypes = field(
        default=None,
        metadata={
            "name": "PropertyDataTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    medium_types: None | MasterDataMediumTypes = field(
        default=None,
        metadata={
            "name": "MediumTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    mask_versions: None | MasterDataMaskVersions = field(
        default=None,
        metadata={
            "name": "MaskVersions",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    functional_blocks: None | MasterDataFunctionalBlocks = field(
        default=None,
        metadata={
            "name": "FunctionalBlocks",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    product_languages: None | MasterDataProductLanguages = field(
        default=None,
        metadata={
            "name": "ProductLanguages",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    manufacturers: None | MasterDataManufacturers = field(
        default=None,
        metadata={
            "name": "Manufacturers",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    languages: None | MasterDataLanguages = field(
        default=None,
        metadata={
            "name": "Languages",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
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
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
