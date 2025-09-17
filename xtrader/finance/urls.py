from django.urls import re_path

from finance import views

urlpatterns = [
    re_path(
        r"^calculate-filter/(?:(?P<interval>\w+)/)?$",
        views.calculate_indicators,
        name="mabna api",
    ),
    re_path(r"^save-strategy", views.save_strategy, name="save-strategy"),
    re_path(
        r"^get-strategy-names",
        views.get_strategy_names,
        name="get-strategy-names",
    ),
    re_path(r"^load-strategy", views.load_strategy, name="load-strategy"),
    re_path(r"^scan-market", views.scan_market, name="scan-market"),

    # watchlist or watch_list?
    # chat-gpt: in your Python code (functions, variables), use watch_list to
    # follow PEP 8. In user-facing or web contexts, watchlist is fine and even
    # preferred for familiarity as "watchlist" is a common concept used in 
    # finance apps.
    re_path(
        r"^update-symbol-to-watchlist",
        views.update_symbol_to_watch_list,
        name="update-symbol-to-watchlist",
    ),
    re_path(
        r"^add-new-watchlist", views.add_new_watch_list, name="add-new-watchlist"
    ),
    re_path(r"^get-watchlists", views.get_watch_lists, name="get-watchlists"),
    re_path(
        r"^strategy-notif/(?:(?P<interval>\w+)/)?$",
        views.strategy_notif,
        name="strategy-notif",
    ),
    re_path(r"^market-watch", views.market_watch, name="market-watch"),
    re_path(r"^get-filters", views.get_filters, name="get-filters"),
    re_path(r"^filter-market", views.filter_market, name="filter-market"),
    re_path(r"^indicators-api", views.indicators_api, name="indicators-api"),
    re_path(r"^robots", views.display, name="backtest"), # TODO: name?
    re_path(r"^back-test", views.back_test, name="back-test"),
    re_path(r"^about-us", views.about_us, name="about-us"),
    re_path(r"^$", views.index, name="index"),
    re_path(
        r"^stock-watch/(?:(?P<symbol_id>\w+)/)?$",
        views.stock_watch,
        name="stock-watch",
    ),
    re_path(r"^spot/(?:(?P<symbol_id>\w+)/)?$", views.spot, name="spot"),
    re_path(
        r"^.well-known/acme-challenge/S40flyGXu3pwdfdYzH-MLgUCromgJXv8WMbnAO_LXwE",
        views.ssl,
        name="ssl",
    ),  # TODO: what is this? 
    re_path(r"^trade", views.trade, name="trade"),
    re_path(r"^trading-view", views.trading_view, name="trading_view"),
    re_path(
        r"^webhook/(?P<token>[\w-]+)",
        views.trading_view_trade,
        name="trading-view-trade",
    ),
    re_path(r"^portfolio", views.portfolio, name="portfolio"),
    re_path(r"^orders", views.get_orders, name="orders"),
    # Setup profile
    re_path(r"^profile-settings/$", views.profile_settings, name="profile-settings"),
    re_path(r"^save-exchange", views.save_exchange, name="add-exchange"),
    re_path(r"^remove-exchange", views.remove_exchange, name="remove-exchange"),
    re_path(r"^get-exchanges", views.get_exchanges, name="get-exchange"),
    re_path(r"^cancel-order", views.cancel_order, name="cancel-order"),
    re_path(r"^martingale-strategy", views.run_martingale_strategy, name="martingale-strategy"),
    re_path(r"^test-volume", views.test_volume, name="test-volume"),
    re_path(r"^test-api", views.test_api, name="test-api"),
    re_path(
        r"^telegram-webhook", views.telegram_webhook, name="telegram-webhook"
    ),
]
