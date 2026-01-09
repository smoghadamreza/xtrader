from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class IndicatorConfig:
    """
    Configuration for initializing an Indicator.
    """
    symbol: str
    interval: str
    lookback: Optional[int] = None          # Some indicators require a lookback period
    params: Dict[str, Any] = field(default_factory=dict)

class IndicatorTypes(str, Enum):
    MAIN = "main"
    MINOR = "minor"
    ASCENDING = "ascending"
    SPECIAL = "special"
    CANDLESTICK = "candlestick"
    CROSS = "cross"
    ADVANCE_CROSS = "advance_cross"

    @classmethod
    def all(cls) -> list[str]:
        return [member.value for member in cls]

    @classmethod
    def is_valid(cls, indicator_type: str) -> bool:
        return indicator_type.lower() in cls._value2member_map_
