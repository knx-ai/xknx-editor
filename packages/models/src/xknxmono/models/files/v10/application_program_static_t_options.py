from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.application_program_static_t_options_parameter_byte_order import (
    ApplicationProgramStaticOptionsParameterByteOrder,
)
from xknxmono.models.files.v10.text_encoding_t import TextEncoding

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticOptions:
    class Meta:
        global_type = False

    prefer_partial_download_if_application_loaded: bool = field(
        default=False,
        metadata={
            "name": "PreferPartialDownloadIfApplicationLoaded",
            "type": "Attribute",
        },
    )
    easy_ctrl_mode_mode_style_empty_group_com_tables: bool = field(
        default=False,
        metadata={
            "name": "EasyCtrlModeModeStyleEmptyGroupComTables",
            "type": "Attribute",
        },
    )
    set_object_table_length_always_to_one: bool = field(
        default=False,
        metadata={
            "name": "SetObjectTableLengthAlwaysToOne",
            "type": "Attribute",
        },
    )
    text_parameter_encoding: None | TextEncoding = field(
        default=None,
        metadata={
            "name": "TextParameterEncoding",
            "type": "Attribute",
        },
    )
    text_parameter_zero_terminate: bool = field(
        default=False,
        metadata={
            "name": "TextParameterZeroTerminate",
            "type": "Attribute",
        },
    )
    parameter_byte_order: ApplicationProgramStaticOptionsParameterByteOrder = field(
        default=ApplicationProgramStaticOptionsParameterByteOrder.BIG_ENDIAN,
        metadata={
            "name": "ParameterByteOrder",
            "type": "Attribute",
        },
    )
    partial_download_only_visible_parameters: bool = field(
        default=False,
        metadata={
            "name": "PartialDownloadOnlyVisibleParameters",
            "type": "Attribute",
        },
    )
    legacy_no_partial_download: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoPartialDownload",
            "type": "Attribute",
        },
    )
    legacy_no_memory_verify_mode: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoMemoryVerifyMode",
            "type": "Attribute",
        },
    )
    legacy_no_optimistic_write: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoOptimisticWrite",
            "type": "Attribute",
        },
    )
    legacy_do_not_report_property_write_errors: bool = field(
        default=False,
        metadata={
            "name": "LegacyDoNotReportPropertyWriteErrors",
            "type": "Attribute",
        },
    )
    legacy_no_background_download: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoBackgroundDownload",
            "type": "Attribute",
        },
    )
    legacy_do_not_check_manufacturer_id: bool = field(
        default=False,
        metadata={
            "name": "LegacyDoNotCheckManufacturerId",
            "type": "Attribute",
        },
    )
    legacy_always_reload_app_if_co_visibility_changed: bool = field(
        default=False,
        metadata={
            "name": "LegacyAlwaysReloadAppIfCoVisibilityChanged",
            "type": "Attribute",
        },
    )
    legacy_never_reload_app_if_co_visibility_changed: bool = field(
        default=False,
        metadata={
            "name": "LegacyNeverReloadAppIfCoVisibilityChanged",
            "type": "Attribute",
        },
    )
    legacy_do_not_support_undo_delete: bool = field(
        default=False,
        metadata={
            "name": "LegacyDoNotSupportUndoDelete",
            "type": "Attribute",
        },
    )
    legacy_allow_partial_download_if_ap2_mismatch: bool = field(
        default=False,
        metadata={
            "name": "LegacyAllowPartialDownloadIfAp2Mismatch",
            "type": "Attribute",
        },
    )
    legacy_keep_object_table_gaps: bool = field(
        default=False,
        metadata={
            "name": "LegacyKeepObjectTableGaps",
            "type": "Attribute",
        },
    )
    legacy_proxy_communication_objects: bool = field(
        default=False,
        metadata={
            "name": "LegacyProxyCommunicationObjects",
            "type": "Attribute",
        },
    )
    device_info_ignore_run_state: bool = field(
        default=False,
        metadata={
            "name": "DeviceInfoIgnoreRunState",
            "type": "Attribute",
        },
    )
    device_info_ignore_loaded_state: bool = field(
        default=False,
        metadata={
            "name": "DeviceInfoIgnoreLoadedState",
            "type": "Attribute",
        },
    )
    device_compare_allow_compatible_manufacturer_id: bool = field(
        default=False,
        metadata={
            "name": "DeviceCompareAllowCompatibleManufacturerId",
            "type": "Attribute",
        },
    )
