from typing import List

from finance.exchange.data import AccountSnapshot
from finance.exchange.factory import ExchangeServiceFactory
from finance.exchange.base import BaseExchangeService
from django.contrib.auth.models import User
from .models import ProTrader
from finance.exchange.exception import NoConnectedExchangeException
from .exception import NoProTraderForThisUser, NoExchangeServiceForProTrader
from utils.unix_millis import UnixMillis


class ProTraderService:

    def __init__(self, user: User):
        try:
            self._pro_trader = ProTrader.objects.get(trader=user)
            self._exchange_service = ExchangeServiceFactory.get_service_for_user(
                user=user
            )
        except ProTrader.DoesNotExist:
            raise NoProTraderForThisUser
        except NoConnectedExchangeException:
            raise NoExchangeServiceForProTrader

    def get_recent_nav_snapshots(self) -> List[AccountSnapshot]:  # replaces legacy ProTrader.get_history
        return self._exchange_service.get_recent_nav_snapshots()
    
    def get_records(self):
        recent_nav_snapshots = self.get_recent_nav_snapshots()

        time_to_btc_total = {
            record.update_time_timestamp_ms: record.total_asset_of_btc
            for record in recent_nav_snapshots    
        }
        params = {"symbol": "BTCUSDT", "interval": "1d", "limit": 50}
        candles = self._exchange_service.get_candles(params=params)
        h = []
        btc = []
        for candle in candles:
            close_time = UnixMillis.normalize_to_milli_second(ts_ms=candle.close_time)
            if close_time in time_to_btc_total:
                btc_total = time_to_btc_total[close_time]
                h.append([close_time, round(btc_total * candle.close_price, 2)])
                btc.append([close_time, round(candle.close_price, 2)])
        return {"trader": h, "btc": btc}
