from django.urls import re_path

from finance import views

urlpatterns = [
    re_path(
        r"^calculate_filter/(?:(?P<interval>\w+)/)?$",
        views.calculate_indicators,
        name="mabna api",
    ),
    re_path(r"^save_strategy", views.save_strategy, name="save strategy"),
    re_path(
        r"^get_strategy_names",
        views.get_strategy_names,
        name="get strategy names",
    ),
    re_path(r"^load_strategy", views.load_strategy, name="load strategy"),
    re_path(r"^scan_market", views.scan_market, name="scan market"),
    re_path(
        r"^updateSymbol2Watchlist",
        views.update_symbol2watchlist,
        name="updateSymbol2Watchlist",
    ),
    re_path(
        r"^addNewWatchList", views.add_new_watch_list, name="addNewWatchList"
    ),
    re_path(r"^getWatchLists", views.get_watch_lists, name="getWatchLists"),
    re_path(
        r"^strategyNotif/(?:(?P<interval>\w+)/)?$",
        views.strategy_notif,
        name="strategyNotif",
    ),
    re_path(r"^marketwatch", views.market_watch, name="marketwatch"),
    re_path(r"^getfilters", views.getfilters, name="getfilters"),
    re_path(r"^filtermarket", views.filtermarket, name="filtermarket"),
    re_path(r"^indicators-api", views.indicators_api, name="indicatoss_api"),
    re_path(r"^robots", views.display, name="backtest"),
    re_path(r"^back-test", views.back_test, name="back_test"),
    re_path(r"^about-us", views.about_us, name="about_us"),
    re_path(r"^$", views.index, name="index"),
    re_path(
        r"^stockwatch/(?:(?P<SymbolId>\w+)/)?$",
        views.stockwatch,
        name="stockwatch",
    ),
    re_path(r"^spot/(?:(?P<symbol_id>\w+)/)?$", views.spot, name="spot"),
    re_path(
        r"^.well-known/acme-challenge/S40flyGXu3pwdfdYzH-MLgUCromgJXv8WMbnAO_LXwE",
        views.ssl,
        name="ssl",
    ),
    re_path(r"^trade", views.trade, name="trade"),
    re_path(r"^tradingview", views.tradingview, name="tradingview"),
    re_path(
        r"^webhook/(?P<token>[\w-]+)",
        views.tradingview_trade,
        name="tradingviewTrade",
    ),
    re_path(r"^portfo", views.portfo, name="portfo"),
    re_path(r"^orders", views.get_orders, name="orders"),
    # Setup profile
    re_path(r"^profile/setup/$", views.profile_setup, name="profile_setup"),
    re_path(r"^addExchange", views.save_exchange, name="saveExchange"),
    re_path(r"^removeExchange", views.remove_exchange, name="removeExchange"),
    re_path(r"^getExchanges", views.get_exchanges, name="getExchange"),
    re_path(r"^cancelOrder", views.cancelOrder, name="cancelOrder"),
    re_path(r"^statusaccount", views.account_status, name="status"),
    re_path(r"^volume", views.manage_volume, name="mange volume"),
    re_path(r"^testvolume", views.test_volume, name="test volume"),
    re_path(r"^testAPI", views.testAPI, name="testAPI"),
    re_path(
        r"^telegram/webhook", views.telegram_webhook, name="telegram_webhook"
    ),
]
