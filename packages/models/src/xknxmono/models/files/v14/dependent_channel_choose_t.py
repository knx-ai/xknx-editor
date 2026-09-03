from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.application_program_channel_t import (
    ApplicationProgramChannel,
)
from xknxmono.models.files.v14.rename_t import Rename
from xknxmono.models.files.v14.when_t import When

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class DependentChannelChoose:
    """
    :ivar when: registration-relevant list
    :ivar param_ref_id: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "DependentChannelChoose_t"

    when: list[DependentChannelChooseWhen] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
    param_ref_id: str = field(
        metadata={
            "name": "ParamRefId",
            "type": "Attribute",
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class DependentChannelChooseWhen(When):
    class Meta:
        global_type = False

    choice: list[ApplicationProgramChannel | DependentChannelChoose | Rename] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "choose",
                    "type": DependentChannelChoose,
                    "namespace": "http://knx.org/xml/project/14",
                },
                {
                    "name": "Rename",
                    "type": Rename,
                    "namespace": "http://knx.org/xml/project/14",
                },
            ),
        },
    )
