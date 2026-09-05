from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.files.v21.ld_ctrl_abs_segment_t import LdCtrlAbsSegment
from xknxeditor.namespaces.files.v21.ld_ctrl_base_choose_t import LdCtrlBaseChoose
from xknxeditor.namespaces.files.v21.ld_ctrl_clear_cached_object_types_t import (
    LdCtrlClearCachedObjectTypes,
)
from xknxeditor.namespaces.files.v21.ld_ctrl_clear_lcfilter_table_t import (
    LdCtrlClearLcfilterTable,
)
from xknxeditor.namespaces.files.v21.ld_ctrl_compare_mem_t import LdCtrlCompareMem
from xknxeditor.namespaces.files.v21.ld_ctrl_compare_prop_t import LdCtrlCompareProp
from xknxeditor.namespaces.files.v21.ld_ctrl_compare_rel_mem_t import LdCtrlCompareRelMem
from xknxeditor.namespaces.files.v21.ld_ctrl_connect_t import LdCtrlConnect
from xknxeditor.namespaces.files.v21.ld_ctrl_declare_prop_desc_t import LdCtrlDeclarePropDesc
from xknxeditor.namespaces.files.v21.ld_ctrl_delay_t import LdCtrlDelay
from xknxeditor.namespaces.files.v21.ld_ctrl_disconnect_t import LdCtrlDisconnect
from xknxeditor.namespaces.files.v21.ld_ctrl_invoke_function_prop_t import (
    LdCtrlInvokeFunctionProp,
)
from xknxeditor.namespaces.files.v21.ld_ctrl_load_completed_t import LdCtrlLoadCompleted
from xknxeditor.namespaces.files.v21.ld_ctrl_load_image_mem_t import LdCtrlLoadImageMem
from xknxeditor.namespaces.files.v21.ld_ctrl_load_image_prop_t import LdCtrlLoadImageProp
from xknxeditor.namespaces.files.v21.ld_ctrl_load_image_rel_mem_t import LdCtrlLoadImageRelMem
from xknxeditor.namespaces.files.v21.ld_ctrl_load_t import LdCtrlLoad
from xknxeditor.namespaces.files.v21.ld_ctrl_map_error_t import LdCtrlMapError
from xknxeditor.namespaces.files.v21.ld_ctrl_master_reset_t import LdCtrlMasterReset
from xknxeditor.namespaces.files.v21.ld_ctrl_max_length_t import LdCtrlMaxLength
from xknxeditor.namespaces.files.v21.ld_ctrl_merge_t import LdCtrlMerge
from xknxeditor.namespaces.files.v21.ld_ctrl_progress_text_t import LdCtrlProgressText
from xknxeditor.namespaces.files.v21.ld_ctrl_read_function_prop_t import (
    LdCtrlReadFunctionProp,
)
from xknxeditor.namespaces.files.v21.ld_ctrl_rel_segment_t import LdCtrlRelSegment
from xknxeditor.namespaces.files.v21.ld_ctrl_restart_t import LdCtrlRestart
from xknxeditor.namespaces.files.v21.ld_ctrl_set_control_variable_t import (
    LdCtrlSetControlVariable,
)
from xknxeditor.namespaces.files.v21.ld_ctrl_task_ctrl1_t import LdCtrlTaskCtrl1
from xknxeditor.namespaces.files.v21.ld_ctrl_task_ctrl2_t import LdCtrlTaskCtrl2
from xknxeditor.namespaces.files.v21.ld_ctrl_task_ptr_t import LdCtrlTaskPtr
from xknxeditor.namespaces.files.v21.ld_ctrl_task_segment_t import LdCtrlTaskSegment
from xknxeditor.namespaces.files.v21.ld_ctrl_unload_t import LdCtrlUnload
from xknxeditor.namespaces.files.v21.ld_ctrl_write_mem_t import LdCtrlWriteMem
from xknxeditor.namespaces.files.v21.ld_ctrl_write_prop_t import LdCtrlWriteProp
from xknxeditor.namespaces.files.v21.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem

__NAMESPACE__ = "http://knx.org/xml/project/21"


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
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlLoad",
                    "type": LdCtrlLoad,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlMaxLength",
                    "type": LdCtrlMaxLength,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlClearCachedObjectTypes",
                    "type": LdCtrlClearCachedObjectTypes,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlLoadCompleted",
                    "type": LdCtrlLoadCompleted,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlAbsSegment",
                    "type": LdCtrlAbsSegment,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlRelSegment",
                    "type": LdCtrlRelSegment,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlTaskSegment",
                    "type": LdCtrlTaskSegment,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlTaskPtr",
                    "type": LdCtrlTaskPtr,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlTaskCtrl1",
                    "type": LdCtrlTaskCtrl1,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlTaskCtrl2",
                    "type": LdCtrlTaskCtrl2,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlWriteProp",
                    "type": LdCtrlWriteProp,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlCompareProp",
                    "type": LdCtrlCompareProp,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlLoadImageProp",
                    "type": LdCtrlLoadImageProp,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlInvokeFunctionProp",
                    "type": LdCtrlInvokeFunctionProp,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlReadFunctionProp",
                    "type": LdCtrlReadFunctionProp,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlWriteMem",
                    "type": LdCtrlWriteMem,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlCompareMem",
                    "type": LdCtrlCompareMem,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlLoadImageMem",
                    "type": LdCtrlLoadImageMem,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlWriteRelMem",
                    "type": LdCtrlWriteRelMem,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlCompareRelMem",
                    "type": LdCtrlCompareRelMem,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlLoadImageRelMem",
                    "type": LdCtrlLoadImageRelMem,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlConnect",
                    "type": LdCtrlConnect,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlDisconnect",
                    "type": LdCtrlDisconnect,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlRestart",
                    "type": LdCtrlRestart,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlMasterReset",
                    "type": LdCtrlMasterReset,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlDelay",
                    "type": LdCtrlDelay,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlSetControlVariable",
                    "type": LdCtrlSetControlVariable,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlMapError",
                    "type": LdCtrlMapError,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlProgressText",
                    "type": LdCtrlProgressText,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlDeclarePropDesc",
                    "type": LdCtrlDeclarePropDesc,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlClearLCFilterTable",
                    "type": LdCtrlClearLcfilterTable,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "LdCtrlMerge",
                    "type": LdCtrlMerge,
                    "namespace": "http://knx.org/xml/project/21",
                },
                {
                    "name": "choose",
                    "type": LdCtrlBaseChoose,
                    "namespace": "http://knx.org/xml/project/21",
                },
            ),
        },
    )
