from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.master_data_t_manufacturers_manufacturer_public_keys_public_key import (
    MasterDataManufacturersManufacturerPublicKeysPublicKey,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerPublicKeys:
    class Meta:
        global_type = False

    public_key: list[MasterDataManufacturersManufacturerPublicKeysPublicKey] = field(
        default_factory=list,
        metadata={
            "name": "PublicKey",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
