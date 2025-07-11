from django.contrib import admin

from .models import BalanceSheet, Income, MarketWatch, Ratio, StockWatch


class stockwatch_admin(admin.ModelAdmin):
    list_display = (
        "instrument_name",
        "company_name",
        "exchange_name",
        "last_trade_date",
        "instrument_state_title",
        "symbol_id",
    )


class balance_sheet_admin(admin.ModelAdmin):
    list_display = (
        "instrument_name",
        "cash",
        "net_receivables",
        "accounts_payable",
        "equity",
        "symbol_id",
    )


class income_admin(admin.ModelAdmin):
    list_display = (
        "instrument_name",
        "total_income",
        "gross_profit",
        "net_income",
        "symbol_id",
    )


class ratio_admin(admin.ModelAdmin):
    list_display = (
        "instrument_name",
        "current_ratio",
        "quick_ratio",
        "cash_ratio",
        "symbol_id",
    )


class marketwatch_admin(admin.ModelAdmin):
    list_display = (
        "get_company_name",
        "get_instrument_name",
        "get_symbol_id",
    )


admin.site.register(StockWatch, stockwatch_admin)
admin.site.register(Ratio, ratio_admin)
admin.site.register(Income, income_admin)
admin.site.register(BalanceSheet, balance_sheet_admin)
admin.site.register(MarketWatch, marketwatch_admin)
