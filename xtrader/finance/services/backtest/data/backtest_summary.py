from dataclasses import dataclass, asdict
from typing import List

@dataclass
class BackTestSummary:
    avg_candles_in_trade: float
    avg_waiting_candles: float
    avg_return: float
    std_candles_in_trade: float
    std_waiting_candles: float
    std_return: float

    def to_dict(self):
        """
        Serialize BackTestSummary to dictionary for client consumption.
        """
        return asdict(self)
