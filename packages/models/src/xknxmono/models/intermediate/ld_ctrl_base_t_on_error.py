from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.ld_ctrl_error_cause_t import LdCtrlErrorCause


@dataclass(slots=True, kw_only=True)
class LdCtrlBaseOnError:
    """
    :ivar cause: registration-relevant
    :ivar ignore: registration-relevant
    :ivar message_ref:
    """

    class Meta:
        global_type = False

    cause: LdCtrlErrorCause = field(
        metadata={
            "name": "Cause",
            "type": "Attribute",
        }
    )
    ignore: bool = field(
        default=False,
        metadata={
            "name": "Ignore",
            "type": "Attribute",
        },
    )
    message_ref: None | str = field(
        default=None,
        metadata={
            "name": "MessageRef",
            "type": "Attribute",
        },
    )
