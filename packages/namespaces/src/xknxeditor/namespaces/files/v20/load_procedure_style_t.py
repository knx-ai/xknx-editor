from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/20"


class LoadProcedureStyle(Enum):
    DEFAULT_PROCEDURE = "DefaultProcedure"
    PRODUCT_PROCEDURE = "ProductProcedure"
    MERGED_PROCEDURE = "MergedProcedure"
