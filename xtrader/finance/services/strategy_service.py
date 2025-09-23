import json
import logging
from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.contrib.auth.models import User

from sales.models import Subscription
from finance.exceptions import (
    SubscriptionUpgradeNeededForCreatingStrategy as SubUpgradeNeededException,
    StrategyWasNotFound
)
from finance.models import Strategy, Watchlist
from finance.services.data import (
    StrategyCreationParams, StrategyModificationResult,
    StrategyAction, StrategyConfig, StrategyRecord,
    SubscriptionLimits
)

logger = logging.getLogger(__name__)


class StrategyService:
    """
    Service centered on a trader (User). Loads strategies as a QuerySet on init.
    Writes reload that QuerySet after create/delete so it remains current.
    """

    def __init__(self, trader: User) -> None:
        self.trader = trader

    @property
    def strategies(self) -> QuerySet[Strategy]:
        return Strategy.objects.filter(trader=self.trader)

    def add_or_update_strategy(self, raw_data: Dict[str, Any]) -> StrategyModificationResult:
        """
        Create/update/delete based on incoming params.
        - If params.filters is falsy (None or empty list) -> delete.
        - On create, enforce subscription limits; raise SubscriptionUpgradeNeeded if exceeded.
        Returns a StrategyModificationResult with a bounded action enum.
        """
        params = StrategyCreationParams.from_dict(raw_data)

        existing = self._find_strategy_in_qs(params.id)
        if existing:
            return self._update_or_delete_existing(existing, params)

        if not params.filters:
            return StrategyModificationResult(action=StrategyAction.DELETE, id=params.id)

        if not self._can_create_strategy():
            raise SubUpgradeNeededException()

        watchlist = self._resolve_watchlist(params.watchlist_id)
        new_strategy = Strategy.objects.create(
            trader=self.trader,
            name=params.name,
            filters=json.dumps(params.filters),
            watchlist=watchlist,
            interval=params.interval,
        )
        return StrategyModificationResult(action=StrategyAction.CREATE, id=new_strategy.pk)

    def get_strategy(self, strategy_id: int) -> StrategyConfig:
        strategy = self._find_strategy_in_qs(strategy_id=strategy_id)
        if strategy is None:
            raise StrategyWasNotFound(strategy_id=strategy_id)

        filters_raw = strategy.filters
        try:
            parsed = json.loads(filters_raw) if isinstance(filters_raw, str) else (filters_raw or [])
        except Exception:
            logger.exception("Failed to parse filters for strategy_id=%s", strategy_id)
            parsed = []

        watchlist_id = str(strategy.watchlist.pk) if strategy.watchlist else "0"
        return StrategyConfig(filters=parsed, watchlist_id=watchlist_id, interval=strategy.interval)

    def get_strategies(self) -> List[StrategyRecord]:
        return [StrategyRecord(id=s.pk, name=s.name)for s in self.strategies]

    def get_strategy_counts(self) -> int:
        return self.strategies.count()

    def get_pack_limit(self) -> SubscriptionLimits:
        sub = Subscription.have_subscribe(self.trader)
        if not sub:
            return SubscriptionLimits(strategy=1, watchlist=0)
        return SubscriptionLimits(strategy=sub.package.limit, watchlist=sub.package.limit)

    def _find_strategy_in_qs(self, strategy_id: Optional[int]) -> Optional[Strategy]:
        """Attempt to find a strategy in the QuerySet without extra DB hits if possible."""
        if strategy_id is None:
            return None
        try:
            # QuerySet.get() will hit DB, but it's okay if our QS isn't evaluated.
            return self.strategies.filter(pk=strategy_id).first()
        except Exception:
            return None

    def _update_or_delete_existing(self, strategy: Strategy, params: StrategyCreationParams) -> StrategyModificationResult:
        """
        Update or delete a pre-loaded strategy instance.
        - falsy filters => delete
        - otherwise update persisted JSON filters and fields
        """
        if not params.filters:
            strategy.delete()
            return StrategyModificationResult(action=StrategyAction.DELETE, id=params.id)

        strategy.name = params.name
        strategy.filters = json.dumps(params.filters)
        strategy.interval = params.interval
        watchlist = self._resolve_watchlist(params.watchlist_id)
        if watchlist is not None:
            strategy.watchlist = watchlist
        strategy.save(
            update_fields=[
                "name", "filters",
                "interval", "watchlist"
            ]
        )
        return StrategyModificationResult(action=StrategyAction.UPDATE, id=strategy.pk)


    def _resolve_watchlist(self, watchlist_id: Union[str, int, None]) -> Optional[Watchlist]:
        if watchlist_id is None:
            return None
        try:
            wl_id = int(watchlist_id)
        except (ValueError, TypeError):
            return None
        return Watchlist.objects.filter(user=self.trader, id=wl_id).first()

    def _can_create_strategy(self) -> bool:
        limits = self.get_pack_limit()
        return self.get_strategy_counts() < int(limits.strategy)
