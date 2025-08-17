from django.urls import re_path

import data.views as views

urlpatterns = [
    re_path(r"^symbols", views.get_symbols, name="get-symbols"),
    re_path(r"^all-symbols", views.get_all_symbols, name="all-symbols"),
    re_path(r"^intervals/$", views.get_intervals, name="get-intervals"),
     # TODO: I suspect this endpoint is never being used. 
     # I will change it to something else to see if the project encounter problems. 
     # Previous name: r"^history/$"
    re_path(r"^this-is-not-being-used/$", views.get_all_symbol_candles_history), 
    re_path(r"^stock-watch/(?P<symbol_id>\w+)/$", views.stock_watch_info),
    re_path(
        r"^symbol-search/q=(?P<query>\w+)",
        views.symbol_search,
        name="symbol-search",
    ),
    re_path(
        r"^candles-history/(?P<symbol_id>\w+)/(?P<interval>\w+)",
        views.get_symbol_candles_history,
        name="candles-history",
    ),
]
