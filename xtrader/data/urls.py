from django.urls import re_path

import data.views as views

urlpatterns = [
    re_path(r"^symbols", views.get_symbols, name="get-symbols"),
    re_path(r"^all-symbols", views.get_all_symbols, name="all-symbols"),
    re_path(r"^intervals/$", views.get_intervals, name="get-intervals"),
    re_path(r"^history/$", views.history),
    re_path(r"^stock-watch/(?P<symbol_id>\w+)/$", views.stock_watch_info),
    re_path(
        r"^symbol-search/q=(?P<query>\w+)",
        views.symbol_search,
        name="symbol-search",
    ),
    re_path(
        r"^get-data/(?P<symbol_id>\w+)/(?P<interval>\w+)",
        views.get_data,
        name="get-data",
    ),
]
