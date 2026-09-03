from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.master_data_t_datapoint_roles import (
    MasterDataDatapointRoles,
)
from xknxmono.models.intermediate.master_data_t_datapoint_types import (
    MasterDataDatapointTypes,
)
from xknxmono.models.intermediate.master_data_t_function_types import (
    MasterDataFunctionTypes,
)
from xknxmono.models.intermediate.master_data_t_functional_blocks import (
    MasterDataFunctionalBlocks,
)
from xknxmono.models.intermediate.master_data_t_interface_object_properties import (
    MasterDataInterfaceObjectProperties,
)
from xknxmono.models.intermediate.master_data_t_interface_object_types import (
    MasterDataInterfaceObjectTypes,
)
from xknxmono.models.intermediate.master_data_t_languages import MasterDataLanguages
from xknxmono.models.intermediate.master_data_t_manufacturers import (
    MasterDataManufacturers,
)
from xknxmono.models.intermediate.master_data_t_mask_versions import (
    MasterDataMaskVersions,
)
from xknxmono.models.intermediate.master_data_t_medium_types import (
    MasterDataMediumTypes,
)
from xknxmono.models.intermediate.master_data_t_product_languages import (
    MasterDataProductLanguages,
)
from xknxmono.models.intermediate.master_data_t_property_data_types import (
    MasterDataPropertyDataTypes,
)
from xknxmono.models.intermediate.master_data_t_space_usages import (
    MasterDataSpaceUsages,
)


@dataclass(slots=True, kw_only=True)
class MasterData:
    class Meta:
        name = "MasterData_t"

    datapoint_types: None | MasterDataDatapointTypes = field(
        default=None,
        metadata={
            "name": "DatapointTypes",
            "type": "Element",
        },
    )
    datapoint_roles: None | MasterDataDatapointRoles = field(
        default=None,
        metadata={
            "name": "DatapointRoles",
            "type": "Element",
        },
    )
    interface_object_types: None | MasterDataInterfaceObjectTypes = field(
        default=None,
        metadata={
            "name": "InterfaceObjectTypes",
            "type": "Element",
        },
    )
    interface_object_properties: None | MasterDataInterfaceObjectProperties = field(
        default=None,
        metadata={
            "name": "InterfaceObjectProperties",
            "type": "Element",
        },
    )
    property_data_types: None | MasterDataPropertyDataTypes = field(
        default=None,
        metadata={
            "name": "PropertyDataTypes",
            "type": "Element",
        },
    )
    medium_types: None | MasterDataMediumTypes = field(
        default=None,
        metadata={
            "name": "MediumTypes",
            "type": "Element",
        },
    )
    mask_versions: None | MasterDataMaskVersions = field(
        default=None,
        metadata={
            "name": "MaskVersions",
            "type": "Element",
        },
    )
    functional_blocks: None | MasterDataFunctionalBlocks = field(
        default=None,
        metadata={
            "name": "FunctionalBlocks",
            "type": "Element",
        },
    )
    product_languages: None | MasterDataProductLanguages = field(
        default=None,
        metadata={
            "name": "ProductLanguages",
            "type": "Element",
        },
    )
    function_types: None | MasterDataFunctionTypes = field(
        default=None,
        metadata={
            "name": "FunctionTypes",
            "type": "Element",
        },
    )
    space_usages: None | MasterDataSpaceUsages = field(
        default=None,
        metadata={
            "name": "SpaceUsages",
            "type": "Element",
        },
    )
    manufacturers: None | MasterDataManufacturers = field(
        default=None,
        metadata={
            "name": "Manufacturers",
            "type": "Element",
        },
    )
    languages: None | MasterDataLanguages = field(
        default=None,
        metadata={
            "name": "Languages",
            "type": "Element",
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
