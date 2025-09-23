from dataclasses import dataclass
from typing import Optional, Any, Dict
from .order import Order


@dataclass
class Trade:
    buy: Order
    sell: Optional[Order] = None

    def is_closed(self) -> bool:
        return self.sell is not None

    def to_dict(self) -> Dict:
        d = {"buy": self.buy.to_dict()}
        if self.sell:
            d["sell"] = self.sell.to_dict()
        return d
