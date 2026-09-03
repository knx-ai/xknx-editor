from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.application_program_channel_t import (
    ApplicationProgramChannel,
    Repeat,
)
from xknxmono.models.intermediate.module_t import Module
from xknxmono.models.intermediate.rename_t import Rename
from xknxmono.models.intermediate.when_t import When


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

    choice: list[
        ApplicationProgramChannel | DependentChannelChoose | Rename | Module | Repeat
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "Channel",
                    "type": ApplicationProgramChannel,
                },
                {
                    "name": "choose",
                    "type": DependentChannelChoose,
                },
                {
                    "name": "Rename",
                    "type": Rename,
                },
                {
                    "name": "Module",
                    "type": Module,
                },
                {
                    "name": "Repeat",
                    "type": Repeat,
                },
            ),
        },
    )
