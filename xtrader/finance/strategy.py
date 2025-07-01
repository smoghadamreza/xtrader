from sales.models import Subscription

from .models import Strategy, Watchlist


def add_strategy_to_db(data, user):
    watchlist_id = data["watchlistId"]
    if watchlist_id == "0":
        watchlist = None
    else:
        watchlist = Watchlist.objects.filter(
            user=user, id=int(watchlist_id)
        ).first()
    strategy = dict(
        trader=user,
        name=data["name"],
        filters=str(data["filters"]),
        watchlist=watchlist,
        interval=data["interval"],
    )
    strategy_id = data["id"]
    st = Strategy.objects.filter(
        trader=strategy["trader"], id=strategy_id
    ).first()
    result = "save"
    if st:
        if strategy["filters"] == "[]":
            st.delete()
            result = "delete"
        else:
            st.name = strategy["name"]
            st.filters = strategy["filters"]
            st.interval = strategy["interval"]
            st.watchlist = watchlist
            st.save()
    else:
        if not strategy["filters"] == "[]":
            if (
                get_pack_limit(user)["strategy"]
                >= get_strategy_counts(user) + 1
            ):
                st = Strategy(**strategy)
                st.save()
                strategy_id = st.id
            else:
                return {
                    "redirect": "/profile/setup/?s=packages",
                    "s": 302,
                    "m": "برای ساخت استراژی جدید به نیاز به ارتقا اشتراک دارید.",
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
    filters = strategy.filters if strategy else "[]"
    interval = strategy.interval if strategy else "4h"
    watchlist_id = 0
    try:
        watchlist_id = strategy.watchlist.id
    except Exception:
        pass
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
    else:
        return {"strategy": sub.package.limit, "watchlist": sub.package.limit}


def get_watchlist_counts(user):
    return len(Watchlist.objects.filter(user=user))
