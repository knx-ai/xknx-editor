from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.trade_t import Trade


@dataclass(slots=True, kw_only=True)
class Trades:
    class Meta:
        name = "Trades_t"

    trade: list[Trade] = field(
        default_factory=list,
        metadata={
            "name": "Trade",
            "type": "Element",
        },
    )
