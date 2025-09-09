from django.contrib import admin

from .models import Exchange, Strategy, TradingView, Watchlist, WatchlistSymbol


class StrategyAdmin(admin.ModelAdmin):
    list_display = ("trader", "interval")


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("trader", "name", "public_key")


class TradingViewAdmin(admin.ModelAdmin):
    list_display = ("trader", "webhook", "trading", "notification")


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "updated")


class WatchlistSymbolsAdmin(admin.ModelAdmin):
    list_display = ("watchlist", "symbol", "updated")


admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(TradingView, TradingViewAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(WatchlistSymbol, WatchlistSymbolsAdmin)
