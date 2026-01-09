from django.urls import re_path

from aum import views

urlpatterns = [
    re_path(r"^$", views.management, name="management"),
    re_path(
        r"^issue-or-redeem-unit",
        views.issue_redeem_unit,
        name="issue-or-redeem-unit",
    ),
    re_path(r"^add-investor", views.add_investor, name="add-investor"),
    re_path(
        r"^transactions-history",
        views.transactions_history,
        name="transactions_history",
    ),
    re_path(r"^investors", views.investors, name="investors"),
    re_path(r"^get-fund", views.get_fund, name="get-fund"),
    re_path(
        r"^init-fund-performance",
        views.init_fund_performance,
        name="init-fund-performance",
    ),
    re_path(
        r"^fund-performance",
        views.get_fund_performance,
        name="get-fund-performance",
    ),
]
