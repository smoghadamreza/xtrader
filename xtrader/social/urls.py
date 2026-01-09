from django.urls import re_path

from social.views import (
    copytrade_views,
    follow_views,
    exchange_views,
    pro_trader_views,
    profile_views,
    public_views
)

urlpatterns = [
    re_path(r"^exchange", exchange_views.exchange, name="saveExchange"),
    re_path(r"^pro-traders", pro_trader_views.get_pro_traders, name="pro-traders"),
    re_path(r"^promote", pro_trader_views.promote_to_pro_trader, name="promote"),
    re_path(r"^copy-trade/follow-toggle/$", follow_views.follow_toggle, name="copy-trade-follow-toggle"),
    re_path(r"^copy-order", copytrade_views.copy_order, name="copy-order"),
    re_path(r"^get-publics", public_views.get_publics, name="get-publics"),
    re_path(r"^copy-trading", profile_views.copy_trading, name="copy-trading"),
    re_path(r"^trader", profile_views.trader, name="trader"),
    re_path(
        r"^get-profile/(?P<pro_id>\w+)", profile_views.get_profile, name="get-profile"
    ),
    re_path(r"^league", profile_views.league, name="league"),
]
