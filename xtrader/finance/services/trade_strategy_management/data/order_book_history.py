from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class OrderBookHistory:
    close: List[float]
    high: List[float]
    date: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, List[Any]]) -> "OrderBookHistory":
        return cls(
            close=data.get("close", []),
            high=data.get("high", []),
            date=data.get("date", []),
        )
