from typing import Literal, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class TradeRecord:
    """Represents a single trade action in the BuyVolumeDecrease strategy."""

    price: float
    volume: int
    action: Literal["initial_buy", "rebuy", "sell_exit"]
    realized_profit_loss: float
    cash_balance: float
    day_index: int

    # Persian translation mapping
    ACTION_TRANSLATION = {
        "initial_buy": "خرید اولیه",
        "rebuy": "خرید مجدد",
        "sell_exit": "فروش خروج",
    }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TradeRecord":
        # Translate action from Persian back to English if needed
        reverse_map = {v: k for k, v in cls.ACTION_TRANSLATION.items()}
        if "action" in data and data["action"] in reverse_map:
            data["action"] = reverse_map[data["action"]]
        return cls(**data)

    def to_dict(self, translate_action: bool = False) -> Dict[str, Any]:
        """Convert to dict; optionally translate `action` to Persian."""
        d = asdict(self)
        if translate_action:
            d["action"] = self.ACTION_TRANSLATION.get(d["action"], d["action"])
        return d
