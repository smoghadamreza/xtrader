from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class FundPerformanceSnapshot:
    age: int
    nav: float
    date: date
    return_percentage: float
    btc: Optional[float] = None
    btc_return_percentage: Optional[float] = None
