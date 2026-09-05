from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/13"


class MasterDataManufacturersManufacturerImportRestriction(Enum):
    OWN = "Own"
    ANY = "Any"
    GROUP = "Group"
