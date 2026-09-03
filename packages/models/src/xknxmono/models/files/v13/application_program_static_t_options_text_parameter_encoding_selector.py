from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/13"


class ApplicationProgramStaticOptionsTextParameterEncodingSelector(Enum):
    USE_WINDOWS_ANSI_CODE_PAGE = "UseWindowsAnsiCodePage"
    USE_PROJECT_CODE_PAGE = "UseProjectCodePage"
    USE_TEXT_PARAMETER_ENCODING_CODE_PAGE = "UseTextParameterEncodingCodePage"
