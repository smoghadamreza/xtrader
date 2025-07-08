from django.urls import re_path

from social import views

urlpatterns = [
    re_path(r"^exchange", views.exchange, name="saveExchange"),
    re_path(r"^protraders", views.pro_traders, name="protraders"),
    re_path(r"^copytrading", views.copytrading, name="copytrading"),
    re_path(r"^copytrade", views.follow_unfollow, name="copytrade"),
    re_path(r"^copyorder", views.copy_order, name="copyorder"),
    re_path(r"^getpublics", views.getpublics, name="getpublics"),
    re_path(r"^promote", views.promote, name="promote"),
    re_path(r"^trader", views.trader, name="trader"),
    re_path(
        r"^getProfile/(?P<pro_id>\w+)", views.get_profile, name="getProfile"
    ),
    re_path(r"^league", views.league, name="league"),
]
