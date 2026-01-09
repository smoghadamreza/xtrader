from dataclasses import dataclass, asdict, field
from typing import List, Any, Dict


@dataclass
class StrategyConfig:
    filters: List[Any] = field(default_factory=list)
    watchlist_id: str = "0"
    interval: str = "4h"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
