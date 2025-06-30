from django.urls import re_path

from aum import views

urlpatterns = [
    re_path(r'^$', views.management, name='management'),
    re_path(r'^issueOrRedeemUnit', views.issue_redeem_unit, name='issueOrRedeemUnit'),
    re_path(r'^redeemUnit', views.redeem_unit, name='redeemUnit'),
    re_path(r'^addInvestor', views.add_investor, name='addInvestor'),
    re_path(r'^transactionsHistory', views.transactions_history, name='transactions_history'),
    re_path(r'^investors', views.investors, name='investors'),
    re_path(r'^getFund', views.get_fund, name='getFund'),
    re_path(r'^initFundPerformance', views.init_fund_performance, name='initFundPerformance'),
    re_path(r'^fundPerformance', views.get_fund_performance, name='getFundPerformance'),
]
