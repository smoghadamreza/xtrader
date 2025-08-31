from typing import List, Optional

from finance.services.exchange.data import AccountSnapshot
from finance.services.exchange.factory import ExchangeServiceFactory
from finance.services.exchange.base import BaseExchangeService
from django.contrib.auth.models import User
from .models import ProTrader
from finance.services.exchange.exception import NoConnectedExchangeException
from .exception import NoProTraderFound, NoExchangeServiceForProTrader
from utils.unix_millis import UnixMillis


class ProTraderService:

    def __init__(self, pro_user: Optional[User] = None, pro_id: Optional[int] = None):
        if not pro_user and not pro_id:
            raise ValueError("Either 'pro_user' or 'pro_id' must be provided.")
        self._pro_user = pro_user
        self._pro_id = pro_id

        try:
            self._set_pro_trader()
            self._exchange_service = ExchangeServiceFactory.get_service_for_user(
                user=self._pro_trader.trader
            )
        except ProTrader.DoesNotExist:
            raise NoProTraderFound()
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
    
    @property
    def pro_trader(self) -> ProTrader:
        return self._pro_trader

    def _set_pro_trader(self) -> None:
        if self._pro_id:
            self._pro_trader = ProTrader.objects.get(pk=self._pro_id)
        elif self._pro_user:
             self._pro_trader = ProTrader.objects.get(trader=self)
        else:
            raise NoProTraderFound()
