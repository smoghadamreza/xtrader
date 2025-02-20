from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from data.models import StockWatch
from uuid import uuid4
from accounts.models import Profile


# Create your models here.
class Watchlist(models.Model):  #TODO: maybe create a watchlist with id=0 to represent all watch-lists and avoid so many if statements.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, blank=True, default='')
    updated = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'{self.user}: {self.name}'


class WatchlistSymbol(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15, null=True, blank=True, default='')
    updated = models.DateTimeField(default=timezone.now, null=True, blank=True)

    @classmethod
    def get_symbols(cls, watchlist_id):
        try:
            watchlist_id = int(watchlist_id)
        except Exception as e:
            return []
        if watchlist_id == 0:
            symbols = StockWatch.objects.all()
            result = [symbol.SymbolId for symbol in symbols]
        else:
            result = [symbol.symbol for symbol in
                      WatchlistSymbol.objects.filter(watchlist__id=watchlist_id).order_by('-updated')]
        return result


class Strategy(models.Model):
    trader = models.ForeignKey(User, related_name='trader', null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=80, default=' استراتژی من ')
    filters = models.TextField()
    config = models.CharField(max_length=500, null=True, blank=True)
    watch_list = models.ForeignKey(Watchlist, null=True, blank=True, on_delete=models.CASCADE)
    interval = models.CharField(max_length=5, null=True, blank=True, default='4h')

    def loads(self):
        strategy_dict = dict(
            filters=[],
            interval=self.interval,
            symbols=self.get_strategy_watchlist_symbols(),
            # TODO: include backtest config
            # config=eval(self.config),
        )
        for filter in eval(self.filters):
            strategy_dict['filters'].append(eval(filter))
        return strategy_dict

    def get_strategy_watchlist_symbols(self):
        watchlist_id = self.get_strategy_watchlist_id()
        return WatchlistSymbol.get_symbols(watchlist_id=watchlist_id)

    def get_strategy_watchlist_id(self):
        try:
            watchlist_id = self.watch_list.id
        except Exception as e:
            watchlist_id = 0
        return watchlist_id


class Exchange(models.Model):
    trader = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, default='myExchange')
    exchange = models.CharField(max_length=80, default='BINANCE')
    public = models.CharField(max_length=500, null=True, blank=True)
    private = models.CharField(max_length=500, null=True, blank=True)


class TradingView(models.Model):
    trader = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    webhook = models.CharField(max_length=80, null=True, blank=True)
    trading = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)

    @staticmethod
    def create_hook():
        # hook = str(uuid4())
        hook = Profile.code_generator(12)
        if TradingView.objects.filter(webhook=hook):
            return TradingView.create_hook()
        return hook

    def activate(self, trading=False, notification=False):
        error = ''
        if trading:
            ex = Exchange.objects.filter(trader=self.trader).first()
            if ex and ex.private and ex.public:
                self.trading = trading
            else:
                error = 'برای فعال کردن ترید، ابتدا باید اکسچنج خود را متصل نمایید'
        else:
            self.trading = trading
        if not error:
            if notification:
                profile = Profile.objects.filter(user=self.trader).first()
                if profile and profile.telegram_id:
                    self.notification = notification
                else:
                    error = '.برای فعال کردن تلگرام، ابتدا باید تلگرام خود را متصل نمایید'
            else:
                self.notification = notification
        if not error:
            self.save()
        return error
