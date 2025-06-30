from django.contrib import admin
from .models import *


class stockwatch_admin(admin.ModelAdmin):
    list_display = (
        'InstrumentName',
        'CompanyName',
        'ExchangeName',
        'LastTradeDate',
        'InstrumentStateTitle',
        'SymbolId',
    )


class balance_sheet_admin(admin.ModelAdmin):
    list_display = (
        'InstrumentName',
        'cash',
        'net_receivables',
        'accounts_payable',
        'equity',
        'SymbolId'
    )


class income_admin(admin.ModelAdmin):
    list_display = (
        'InstrumentName',
        'total_income',
        'gross_profit',
        'net_income',
        'SymbolId',
    )


class ratio_admin(admin.ModelAdmin):
    list_display = (
        'InstrumentName',
        'current_ratio',
        'quick_ratio',
        'cash_ratio',
        'SymbolId',
    )


class marketwatch_admin(admin.ModelAdmin):
    list_display = (
        'get_CompanyName',
        'get_instrument_name',
        'get_SymbolId',
    )


admin.site.register(StockWatch, stockwatch_admin)
admin.site.register(Ratio, ratio_admin)
admin.site.register(Income, income_admin)
admin.site.register(BalanceSheet, balance_sheet_admin)
admin.site.register(MarketWatch, marketwatch_admin)
