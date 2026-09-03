from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.trade_t import Trade

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class Trades:
    class Meta:
        name = "Trades_t"

    trade: list[Trade] = field(
        default_factory=list,
        metadata={
            "name": "Trade",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
