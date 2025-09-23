from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from accounts.exceptions import NoProfileFoundForUser
from data.models import StockWatch
from .exceptions import (
    NoConnectedExchangeException,
    NoConnectedTelegramException
)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=False, blank=True, default="")
    updated = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.name}"


class WatchlistSymbol(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15, null=True, blank=True, default="")
    updated = models.DateTimeField(default=timezone.now, null=True, blank=True)

    @classmethod
    def get_symbols(cls, watchlist_id):
        try:
            watchlist_id = int(watchlist_id)
        except Exception:
            return []
        if watchlist_id == 0:
            symbols = StockWatch.objects.all()
            result = [symbol.symbol_id for symbol in symbols]
        else:
            result = [
                symbol.symbol
                for symbol in WatchlistSymbol.objects.filter(
                    watchlist__id=watchlist_id
                ).order_by("-updated")
            ]
        return result


class Strategy(models.Model):
    trader = models.ForeignKey(
        User,
        related_name="trader",
        null=False,
        blank=True,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=80, default=" استراتژی من ")
    filters = models.TextField()
    config = models.CharField(max_length=500, null=True, blank=True)
    watchlist = models.ForeignKey(
        Watchlist, null=False, blank=True, on_delete=models.CASCADE
    )
    interval = models.CharField(
        max_length=5, null=True, blank=True, default="4h"
    )

    def loads(self):
        strategy_dict: dict[str, Any] = {
            "filters": [],  # Now guaranteed to be List[str]
            "interval": self.interval,
            "symbols": self.get_strategy_watchlist_symbols(),
        }

        temp_filters = strategy_dict["filters"]
        for filter_expr in eval(self.filters):
            temp_filters.append(eval(filter_expr))
        return strategy_dict

    def get_strategy_watchlist_symbols(self):
        watchlist_id = self.get_strategy_watchlist_id()
        return WatchlistSymbol.get_symbols(watchlist_id=watchlist_id)

    def get_strategy_watchlist_id(self) -> int:
        """Returns the watchlist's primary key or 0 if unavailable."""
        if self.watchlist is not None:
            return self.watchlist.pk
        return 0

class ExchangeType(models.TextChoices):
    BINANCE = "BI", _("Binance")
    KUCOIN = "KC", _("KuCoin")
    COINBASE = "CB", _("Coinbase")


class Exchange(models.Model):

    trader = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=80, default="myExchange", unique=True)
    type = models.CharField(
        max_length=20,
        choices=ExchangeType.choices,
        default=ExchangeType.BINANCE,
    )
    public_key = models.CharField(max_length=500, null=False, blank=False)
    private_key = models.CharField(max_length=500, null=False, blank=False)

    @classmethod
    def create_and_verify(cls, trader: User, kwargs: dict):
        from finance.services.exchange.factory import ExchangeServiceFactory



    @classmethod
    def get_exchanges(cls, trader: User):
        exchanges = cls.objects.filter(trader=trader)
        return [
            {
                "exchange": exchange.type,
                "name": exchange.name,
                "public": exchange.public_key,
            } for exchange in exchanges
        ]


    def __str__(self):
        return f"{self.trader} - {self.name} ({self.type})"


class TradingViewIntegration(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The user who owns this TradingView integration."
    )
    webhook_token = models.CharField(
        max_length=80,
        unique=True,
        null=True,
        blank=True,
        help_text="Unique token for validating TradingView webhook requests."
    )
    auto_trading_enabled = models.BooleanField(
        default=False,
        help_text="Whether this user allows incoming TradingView alerts to trigger automated trades."
    )
    telegram_notifications_enabled = models.BooleanField(
        default=False,
        help_text="Whether trade alerts and results are forwarded to the user’s Telegram account."
    )
    
    def update_settings(
        self,
        auto_trading_enabled: bool = False,
        telegram_notifications_enabled: bool = False
    ) -> None:
        """
        Updates auto-trading and Telegram notification settings for this integration.
        Raises exceptions if prerequisites (exchange, profile, telegram) are missing.
        """
        try:
            profile = Profile.objects.get(user=self.user)
            if telegram_notifications_enabled and not profile.telegram_id:
                raise NoConnectedTelegramException()

            exchange = Exchange.objects.get(trader=self.user)
            if (
                auto_trading_enabled and
                (not exchange.private_key or not exchange.public_key)
            ):
                raise NoConnectedExchangeException()

        except Exchange.DoesNotExist:
            if auto_trading_enabled:
                raise NoConnectedExchangeException()
        except Profile.DoesNotExist:
            raise NoProfileFoundForUser()

        self.auto_trading_enabled = auto_trading_enabled
        self.telegram_notifications_enabled = telegram_notifications_enabled

        self.save(update_fields=["auto_trading_enabled", "telegram_notifications_enabled"])

