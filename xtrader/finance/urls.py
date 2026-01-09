from django.urls import re_path

from finance.views import (
    TradingViewIntegrationView,
    TradingViewWebhookView,
    watchlist_views,
    strategy_views,
    base_views,
    market_views,
    exchange_views,
    demo_views
)


urlpatterns = [
    re_path(
        r"^calculate-filter/(?:(?P<interval>\w+)/)?$",
        strategy_views.calculate_indicators,
        name="mabna api",
    ),
    re_path(r"^save-strategy", strategy_views.save_strategy, name="save-strategy"),
    re_path(
        r"^get-strategy-names",
        strategy_views.get_strategy_names,
        name="get-strategy-names",
    ),
    re_path(r"^load-strategy", strategy_views.load_strategy, name="load-strategy"),
    re_path(r"^scan-market", strategy_views.scan_market, name="scan-market"),
    re_path(
        r"^strategy-notif/(?:(?P<interval>\w+)/)?$",
        strategy_views.strategy_notif,
        name="strategy-notif",
    ),
    re_path(r"^martingale-strategy", strategy_views.run_martingale_strategy, name="martingale-strategy"),

    re_path(r"^indicators-api", strategy_views.indicators_api, name="indicators-api"),
    re_path(r"^back-test", strategy_views.back_test, name="back-test"),
    re_path(
        r"^.well-known/acme-challenge/S40flyGXu3pwdfdYzH-MLgUCromgJXv8WMbnAO_LXwE",
        base_views.ssl,
        name="ssl",
    ),
    re_path(r"^settings/$", base_views.profile_settings, name="settings"),
    re_path(r"^about-us", base_views.about_us, name="about-us"),
    re_path(r"^$", base_views.index, name="index"),

    re_path(
        r"^watchlists/modify-symbol$",
        watchlist_views.modify_watchlist_symbol,
        name="modify-watchlist-symbol",
    ),
    re_path(
        r"^watchlists/add$",
        watchlist_views.add_new_watchlist,
        name="add-watchlist",
    ),
    re_path(
        r"^watchlists$",
        watchlist_views.get_watchlists,
        name="get-watchlists",
    ),
    re_path(r"^trading-view$", TradingViewIntegrationView.as_view(), name="trading-view"),
    re_path(r"^webhook/(?P<webhook_token>[\w-]+)$", TradingViewWebhookView.as_view(), name="trading-view-webhook"),

    re_path(r"^market-watch", market_views.market_watch, name="market-watch"),
    re_path(r"^get-filters", market_views.get_filters, name="get-filters"),
    re_path(r"^robots", market_views.display, name="backtest"), # TODO: name?
    re_path(r"^filter-market", market_views.filter_market, name="filter-market"),
    re_path(r"^spot/(?P<symbol_id>\w+)?/?$", market_views.spot, name="spot"),
    re_path(r"^stock-watch/(?P<symbol_id>\w+)?/?$", market_views.stock_watch, name="stock-watch"),
    re_path(r"^portfolio", exchange_views.portfolio, name="portfolio"),
    re_path(r"^save-exchange", exchange_views.save_exchange, name="add-exchange"),
    re_path(r"^remove-exchange", exchange_views.remove_exchange, name="remove-exchange"),
    re_path(r"^get-exchanges", exchange_views.get_exchanges, name="get-exchange"),
    re_path(r"^trade", exchange_views.trade, name="trade"),
    re_path(r"^orders", exchange_views.get_orders, name="orders"),
    re_path(r"^cancel-order", exchange_views.cancel_order, name="cancel-order"),

    re_path(r"^test-volume", demo_views.demo_test_volume, name="test-volume"),
    re_path(r"^test-api", demo_views.demo_test_api, name="test-api"),
]
