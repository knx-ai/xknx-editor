from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_messages_message import (
    ApplicationProgramStaticMessagesMessage,
)


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticMessages:
    class Meta:
        global_type = False

    message: list[ApplicationProgramStaticMessagesMessage] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
        },
    )
