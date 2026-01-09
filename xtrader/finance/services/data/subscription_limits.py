from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class SubscriptionLimits:
    strategy: int = 1
    watchlist: int = 0

    def to_dict(self) -> Dict[str, int]:
        return asdict(self)