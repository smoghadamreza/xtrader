from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from utils.consts import XtraderRequestKeys


@dataclass
class StrategyCreationParams:
    """
    Parameters coming from the frontend for creating/updating a strategy.
    """
    name: str
    watchlist_id: Union[str, int, None]
    interval: str
    id: Optional[int] = None
    filters: List[Any] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrategyCreationParams":
        raw_filters = data.get(XtraderRequestKeys.FILTERS, [])
        filters = raw_filters if isinstance(raw_filters, list) else raw_filters or []

        raw_id = data.get(XtraderRequestKeys.ID)
        try:
            id_val = None if raw_id is None else int(raw_id)
        except (TypeError, ValueError):
            id_val = None

        return cls(
            id=id_val,
            name=str(data.get(XtraderRequestKeys.NAME, "")),
            filters=filters,
            watchlist_id=data.get(XtraderRequestKeys.WATCHLIST_ID, "0"),
            interval=str(data.get(XtraderRequestKeys.INTERVAL, "4h")),
        )

    def filters_as_storage(self) -> str:
        # preserve legacy storage format
        return str(self.filters or "[]")
