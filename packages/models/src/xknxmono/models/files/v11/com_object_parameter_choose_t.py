from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.assign_t import Assign
from xknxmono.models.files.v11.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v11.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v11.parameter_ref_ref_t import ParameterRefRef
from xknxmono.models.files.v11.parameter_separator_t import ParameterSeparator
from xknxmono.models.files.v11.rename_t import Rename
from xknxmono.models.files.v11.when_t import When

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ComObjectParameterChoose:
    """
    :ivar when: registration-relevant list
    :ivar param_ref_id: registration-relevant
    """

    class Meta:
        name = "ComObjectParameterChoose_t"

    when: list[ComObjectParameterChooseWhen] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
            "min_occurs": 1,
        },
    )
    param_ref_id: str = field(
        metadata={
            "name": "ParamRefId",
            "type": "Attribute",
        }
    )


@dataclass(slots=True, kw_only=True)
class ComObjectParameterChooseWhen(When):
    class Meta:
        global_type = False

    choice: list[
        ParameterSeparator
        | ParameterRefRef
        | ComObjectParameterChoose
        | BinaryDataRef
        | ComObjectRefRef
        | Assign
        | Rename
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ParameterSeparator",
                    "type": ParameterSeparator,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "ParameterRefRef",
                    "type": ParameterRefRef,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "choose",
                    "type": ComObjectParameterChoose,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "BinaryDataRef",
                    "type": BinaryDataRef,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "ComObjectRefRef",
                    "type": ComObjectRefRef,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "Assign",
                    "type": Assign,
                    "namespace": "http://knx.org/xml/project/11",
                },
                {
                    "name": "ParameterBlockRename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/11",
                },
            ),
        },
    )
