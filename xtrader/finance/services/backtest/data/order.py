from dataclasses import dataclass, asdict
from typing import Optional, Dict
from enum import Enum


class OrderAction(Enum):
    BUY = "buy"
    SELL = "sell"
    TAKEPROFIT = "takeprofit"
    STOPLOSS = "stoploss"
    NOT_SOLD_YET = "not_sold_yet"


@dataclass
class Order:
    action: OrderAction
    date_index: str
    price: float
    return_percent: float = 0.0
    candles_in_trade: int = 0
    waiting_candles: int = 0
    capital_after_trade: float = 0.0

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["action"] = self.action.value  # convert enum to string
        return d
