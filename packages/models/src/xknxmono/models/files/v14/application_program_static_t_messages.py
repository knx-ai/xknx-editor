from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.application_program_static_t_messages_message import (
    ApplicationProgramStaticMessagesMessage,
)

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticMessages:
    class Meta:
        global_type = False

    message: list[ApplicationProgramStaticMessagesMessage] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
