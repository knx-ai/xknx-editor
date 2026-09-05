from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/11"


class ComObjectSize(Enum):
    VALUE_1_BIT = "1 Bit"
    VALUE_2_BIT = "2 Bit"
    VALUE_3_BIT = "3 Bit"
    VALUE_4_BIT = "4 Bit"
    VALUE_5_BIT = "5 Bit"
    VALUE_6_BIT = "6 Bit"
    VALUE_7_BIT = "7 Bit"
    VALUE_1_BYTE = "1 Byte"
    VALUE_2_BYTES = "2 Bytes"
    VALUE_3_BYTES = "3 Bytes"
    VALUE_4_BYTES = "4 Bytes"
    VALUE_5_BYTES = "5 Bytes"
    VALUE_6_BYTES = "6 Bytes"
    VALUE_7_BYTES = "7 Bytes"
    VALUE_8_BYTES = "8 Bytes"
    VALUE_9_BYTES = "9 Bytes"
    VALUE_10_BYTES = "10 Bytes"
    VALUE_11_BYTES = "11 Bytes"
    VALUE_12_BYTES = "12 Bytes"
    VALUE_14_BYTES = "14 Bytes"
    LEGACY_VAR_DATA = "LegacyVarData"
