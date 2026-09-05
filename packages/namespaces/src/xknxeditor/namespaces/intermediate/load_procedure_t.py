from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.intermediate.ld_ctrl_abs_segment_t import LdCtrlAbsSegment
from xknxeditor.namespaces.intermediate.ld_ctrl_base_choose_t import LdCtrlBaseChoose
from xknxeditor.namespaces.intermediate.ld_ctrl_clear_cached_object_types_t import (
    LdCtrlClearCachedObjectTypes,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_clear_lcfilter_table_t import (
    LdCtrlClearLcfilterTable,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_mem_t import LdCtrlCompareMem
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_prop_t import LdCtrlCompareProp
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_rel_mem_t import LdCtrlCompareRelMem
from xknxeditor.namespaces.intermediate.ld_ctrl_connect_t import LdCtrlConnect
from xknxeditor.namespaces.intermediate.ld_ctrl_declare_prop_desc_t import (
    LdCtrlDeclarePropDesc,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_delay_t import LdCtrlDelay
from xknxeditor.namespaces.intermediate.ld_ctrl_disconnect_t import LdCtrlDisconnect
from xknxeditor.namespaces.intermediate.ld_ctrl_invoke_function_prop_t import (
    LdCtrlInvokeFunctionProp,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_completed_t import LdCtrlLoadCompleted
from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_mem_t import LdCtrlLoadImageMem
from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_prop_t import LdCtrlLoadImageProp
from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_rel_mem_t import (
    LdCtrlLoadImageRelMem,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_t import LdCtrlLoad
from xknxeditor.namespaces.intermediate.ld_ctrl_map_error_t import LdCtrlMapError
from xknxeditor.namespaces.intermediate.ld_ctrl_master_reset_t import LdCtrlMasterReset
from xknxeditor.namespaces.intermediate.ld_ctrl_max_length_t import LdCtrlMaxLength
from xknxeditor.namespaces.intermediate.ld_ctrl_merge_t import LdCtrlMerge
from xknxeditor.namespaces.intermediate.ld_ctrl_progress_text_t import LdCtrlProgressText
from xknxeditor.namespaces.intermediate.ld_ctrl_read_function_prop_t import (
    LdCtrlReadFunctionProp,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_rel_segment_t import LdCtrlRelSegment
from xknxeditor.namespaces.intermediate.ld_ctrl_restart_t import LdCtrlRestart
from xknxeditor.namespaces.intermediate.ld_ctrl_set_control_variable_t import (
    LdCtrlSetControlVariable,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl1_t import LdCtrlTaskCtrl1
from xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl2_t import LdCtrlTaskCtrl2
from xknxeditor.namespaces.intermediate.ld_ctrl_task_ptr_t import LdCtrlTaskPtr
from xknxeditor.namespaces.intermediate.ld_ctrl_task_segment_t import LdCtrlTaskSegment
from xknxeditor.namespaces.intermediate.ld_ctrl_unload_t import LdCtrlUnload
from xknxeditor.namespaces.intermediate.ld_ctrl_write_mem_t import LdCtrlWriteMem
from xknxeditor.namespaces.intermediate.ld_ctrl_write_prop_t import LdCtrlWriteProp
from xknxeditor.namespaces.intermediate.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem


@dataclass(slots=True, kw_only=True)
class LoadProcedure:
    class Meta:
        name = "LoadProcedure_t"

    choice: list[
        LdCtrlUnload
        | LdCtrlLoad
        | LdCtrlMaxLength
        | LdCtrlClearCachedObjectTypes
        | LdCtrlLoadCompleted
        | LdCtrlAbsSegment
        | LdCtrlRelSegment
        | LdCtrlTaskSegment
        | LdCtrlTaskPtr
        | LdCtrlTaskCtrl1
        | LdCtrlTaskCtrl2
        | LdCtrlWriteProp
        | LdCtrlCompareProp
        | LdCtrlLoadImageProp
        | LdCtrlInvokeFunctionProp
        | LdCtrlReadFunctionProp
        | LdCtrlWriteMem
        | LdCtrlCompareMem
        | LdCtrlLoadImageMem
        | LdCtrlWriteRelMem
        | LdCtrlCompareRelMem
        | LdCtrlLoadImageRelMem
        | LdCtrlConnect
        | LdCtrlDisconnect
        | LdCtrlRestart
        | LdCtrlMasterReset
        | LdCtrlDelay
        | LdCtrlSetControlVariable
        | LdCtrlMapError
        | LdCtrlProgressText
        | LdCtrlDeclarePropDesc
        | LdCtrlClearLcfilterTable
        | LdCtrlMerge
        | LdCtrlBaseChoose
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "LdCtrlUnload",
                    "type": LdCtrlUnload,
                },
                {
                    "name": "LdCtrlLoad",
                    "type": LdCtrlLoad,
                },
                {
                    "name": "LdCtrlMaxLength",
                    "type": LdCtrlMaxLength,
                },
                {
                    "name": "LdCtrlClearCachedObjectTypes",
                    "type": LdCtrlClearCachedObjectTypes,
                },
                {
                    "name": "LdCtrlLoadCompleted",
                    "type": LdCtrlLoadCompleted,
                },
                {
                    "name": "LdCtrlAbsSegment",
                    "type": LdCtrlAbsSegment,
                },
                {
                    "name": "LdCtrlRelSegment",
                    "type": LdCtrlRelSegment,
                },
                {
                    "name": "LdCtrlTaskSegment",
                    "type": LdCtrlTaskSegment,
                },
                {
                    "name": "LdCtrlTaskPtr",
                    "type": LdCtrlTaskPtr,
                },
                {
                    "name": "LdCtrlTaskCtrl1",
                    "type": LdCtrlTaskCtrl1,
                },
                {
                    "name": "LdCtrlTaskCtrl2",
                    "type": LdCtrlTaskCtrl2,
                },
                {
                    "name": "LdCtrlWriteProp",
                    "type": LdCtrlWriteProp,
                },
                {
                    "name": "LdCtrlCompareProp",
                    "type": LdCtrlCompareProp,
                },
                {
                    "name": "LdCtrlLoadImageProp",
                    "type": LdCtrlLoadImageProp,
                },
                {
                    "name": "LdCtrlInvokeFunctionProp",
                    "type": LdCtrlInvokeFunctionProp,
                },
                {
                    "name": "LdCtrlReadFunctionProp",
                    "type": LdCtrlReadFunctionProp,
                },
                {
                    "name": "LdCtrlWriteMem",
                    "type": LdCtrlWriteMem,
                },
                {
                    "name": "LdCtrlCompareMem",
                    "type": LdCtrlCompareMem,
                },
                {
                    "name": "LdCtrlLoadImageMem",
                    "type": LdCtrlLoadImageMem,
                },
                {
                    "name": "LdCtrlWriteRelMem",
                    "type": LdCtrlWriteRelMem,
                },
                {
                    "name": "LdCtrlCompareRelMem",
                    "type": LdCtrlCompareRelMem,
                },
                {
                    "name": "LdCtrlLoadImageRelMem",
                    "type": LdCtrlLoadImageRelMem,
                },
                {
                    "name": "LdCtrlConnect",
                    "type": LdCtrlConnect,
                },
                {
                    "name": "LdCtrlDisconnect",
                    "type": LdCtrlDisconnect,
                },
                {
                    "name": "LdCtrlRestart",
                    "type": LdCtrlRestart,
                },
                {
                    "name": "LdCtrlMasterReset",
                    "type": LdCtrlMasterReset,
                },
                {
                    "name": "LdCtrlDelay",
                    "type": LdCtrlDelay,
                },
                {
                    "name": "LdCtrlSetControlVariable",
                    "type": LdCtrlSetControlVariable,
                },
                {
                    "name": "LdCtrlMapError",
                    "type": LdCtrlMapError,
                },
                {
                    "name": "LdCtrlProgressText",
                    "type": LdCtrlProgressText,
                },
                {
                    "name": "LdCtrlDeclarePropDesc",
                    "type": LdCtrlDeclarePropDesc,
                },
                {
                    "name": "LdCtrlClearLCFilterTable",
                    "type": LdCtrlClearLcfilterTable,
                },
                {
                    "name": "LdCtrlMerge",
                    "type": LdCtrlMerge,
                },
                {
                    "name": "choose",
                    "type": LdCtrlBaseChoose,
                },
            ),
        },
    )
