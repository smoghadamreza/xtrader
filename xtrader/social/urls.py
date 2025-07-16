from django.urls import re_path

from social import views

urlpatterns = [
    re_path(r"^exchange", views.exchange, name="saveExchange"),
    re_path(r"^pro-traders", views.pro_traders, name="pro-traders"),
    re_path(r"^copy-trading", views.copy_trading, name="copy-trading"),
    re_path(r"^copy-trade/follow-toggle/$", views.follow_toggle, name="copy-trade-follow-toggle"),
    re_path(r"^copy-order", views.copy_order, name="copy-order"),
    re_path(r"^get-publics", views.get_publics, name="get-publics"),
    re_path(r"^promote", views.promote, name="promote"),
    re_path(r"^trader", views.trader, name="trader"),
    re_path(
        r"^get-profile/(?P<pro_id>\w+)", views.get_profile, name="get-profile"
    ),
    re_path(r"^league", views.league, name="league"),
]
