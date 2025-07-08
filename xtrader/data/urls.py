from django.urls import re_path

import data.views as views

urlpatterns = [
    re_path(r"^symbols", views.get_symbols, name="get_symbols"),
    re_path(r"^allSymbols", views.get_all_symbols, name="allSymbols"),
    re_path(r"^intervals/$", views.get_intervals, name="getIntervals"),
    re_path(r"^history/$", views.history),
    re_path(r"^stockwatch/(?P<SymbolId>\w+)/$", views.stockwatch),
    re_path(
        r"^symbol-search/q=(?P<query>\w+)",
        views.symbol_search,
        name="symbol_search",
    ),
    re_path(
        r"^get-data/(?P<symbol_id>\w+)/(?P<interval>\w+)",
        views.get_data,
        name="get_data",
    ),
]
