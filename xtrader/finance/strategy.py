from typing import Any, Dict, Union, cast

from sales.models import Subscription

from .models import Strategy, Watchlist


def add_strategy_to_db(
    data: Dict[str, Any], user
) -> Dict[str, Union[str, int]]:
    """Add or update a strategy in the database for a given user."""

    watchlist_id = data.get("watchlistId")
    watchlist = None

    if watchlist_id and watchlist_id != "0":
        try:
            watchlist = Watchlist.objects.filter(
                user=user, id=int(watchlist_id)
            ).first()
        except (ValueError, TypeError):
            watchlist = None  # Invalid ID passed; treat as no watchlist

    strategy_data = {
        "trader": user,
        "name": data.get("name", ""),
        "filters": str(data.get("filters", "[]")),
        "watchlist": watchlist,
        "interval": data.get("interval", ""),
    }

    strategy_id = data.get("id")
    if strategy_id is None:
        raise ValueError("Strategy.id cannot be None")
    existing_strategy = Strategy.objects.filter(
        trader=user, id=strategy_id
    ).first()

    result = "save"

    if existing_strategy:
        if strategy_data["filters"] == "[]":
            existing_strategy.delete()
            result = "delete"
        else:
            # Update existing strategy
            existing_strategy.name = strategy_data["name"]
            existing_strategy.filters = strategy_data["filters"]
            existing_strategy.interval = strategy_data["interval"]
            existing_strategy.watchlist = watchlist
            existing_strategy.save()
    else:
        if strategy_data["filters"] != "[]":
            # Check user's strategy limit
            pack_limit = cast(int, get_pack_limit(user).get("strategy", 0))
            strategy_count = get_strategy_counts(user)
            if pack_limit > strategy_count:
                new_strategy = Strategy(**strategy_data)
                new_strategy.save()
                strategy_id = new_strategy.pk
            else:
                return {
                    "redirect": "/profile-settings/?s=packages",
                    "s": 302,
                    "m": "برای ساخت استراتژی جدید به نیاز به ارتقا اشتراک دارید.",
                }
        else:
            result = "delete"

    return {"result": result, "id": strategy_id}


def load_strategy_names(user):
    strategies = Strategy.objects.filter(trader=user).values("name", "id")
    return [
        {"id": strategy["id"], "name": strategy["name"]}
        for strategy in strategies
    ]


def load_strategy_from_db(user, strategy_id):
    strategy = Strategy.objects.filter(trader=user, id=strategy_id).first()
    if not strategy:
        raise ValueError("strategy not found")
    filters = strategy.filters if strategy else "[]"
    interval = strategy.interval if strategy else "4h"

    watchlist_id = 0 if not strategy.watchlist else strategy.watchlist.pk
    return {
        "filters": eval(filters),
        "watchlistId": str(watchlist_id),
        "interval": interval,
    }


def get_strategy_counts(user):
    return len(Strategy.objects.filter(trader=user))


def get_pack_limit(user):
    sub = Subscription.have_subscribe(user)
    if not sub:
        return {"strategy": 1, "watchlist": 0}

    return {"strategy": sub.package.limit, "watchlist": sub.package.limit}


def get_watchlist_counts(user) -> int:
    return len(Watchlist.objects.filter(user=user))
