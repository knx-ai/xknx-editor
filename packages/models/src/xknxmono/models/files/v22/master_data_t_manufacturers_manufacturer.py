from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.master_data_t_manufacturers_manufacturer_datapoint_roles import (
    MasterDataManufacturersManufacturerDatapointRoles,
)
from xknxmono.models.files.v22.master_data_t_manufacturers_manufacturer_datapoint_types import (
    MasterDataManufacturersManufacturerDatapointTypes,
)
from xknxmono.models.files.v22.master_data_t_manufacturers_manufacturer_function_types import (
    MasterDataManufacturersManufacturerFunctionTypes,
)
from xknxmono.models.files.v22.master_data_t_manufacturers_manufacturer_import_restriction import (
    MasterDataManufacturersManufacturerImportRestriction,
)
from xknxmono.models.files.v22.master_data_t_manufacturers_manufacturer_public_keys import (
    MasterDataManufacturersManufacturerPublicKeys,
)
from xknxmono.models.files.v22.master_data_t_manufacturers_manufacturer_space_usages import (
    MasterDataManufacturersManufacturerSpaceUsages,
)
from xknxmono.models.files.v22.member_status_t import MemberStatus

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturer:
    class Meta:
        global_type = False

    order_number_formatting_script: None | str = field(
        default=None,
        metadata={
            "name": "OrderNumberFormattingScript",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    public_keys: None | MasterDataManufacturersManufacturerPublicKeys = field(
        default=None,
        metadata={
            "name": "PublicKeys",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    datapoint_types: None | MasterDataManufacturersManufacturerDatapointTypes = field(
        default=None,
        metadata={
            "name": "DatapointTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    datapoint_roles: None | MasterDataManufacturersManufacturerDatapointRoles = field(
        default=None,
        metadata={
            "name": "DatapointRoles",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    function_types: None | MasterDataManufacturersManufacturerFunctionTypes = field(
        default=None,
        metadata={
            "name": "FunctionTypes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    space_usages: None | MasterDataManufacturersManufacturerSpaceUsages = field(
        default=None,
        metadata={
            "name": "SpaceUsages",
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
    knx_manufacturer_id: int = field(
        metadata={
            "name": "KnxManufacturerId",
            "type": "Attribute",
        }
    )
    default_language: None | str = field(
        default=None,
        metadata={
            "name": "DefaultLanguage",
            "type": "Attribute",
        },
    )
    compatibility_group: None | int = field(
        default=None,
        metadata={
            "name": "CompatibilityGroup",
            "type": "Attribute",
        },
    )
    import_restriction: MasterDataManufacturersManufacturerImportRestriction = field(
        default=MasterDataManufacturersManufacturerImportRestriction.OWN,
        metadata={
            "name": "ImportRestriction",
            "type": "Attribute",
        },
    )
    import_group: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ImportGroup",
            "type": "Attribute",
            "tokens": True,
        },
    )
    order_number_wildcard_character: None | str = field(
        default=None,
        metadata={
            "name": "OrderNumberWildcardCharacter",
            "type": "Attribute",
            "length": 1,
        },
    )
    member_status: MemberStatus = field(
        default=MemberStatus.ACTIVE,
        metadata={
            "name": "MemberStatus",
            "type": "Attribute",
        },
    )
