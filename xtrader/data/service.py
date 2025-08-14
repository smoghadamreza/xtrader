import json
import pandas as pd
from django.utils import timezone
from data.redis import redis_wrapper
from data.redis.constants import RedisNameSpace, SYMBOL_HISTORY_KEYS, INTERVALS
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from data.models import StockWatch
from finance.models import Strategy
from finance.exchange.base import BaseExchangeMarketService
from finance.exchange.binance.service import BinanceMarketService
from utils.unix_millis import UnixMillis



class StockWatchService:
    def __init__(self, market_service: BaseExchangeMarketService = BinanceMarketService()) -> None:
        self._market_service = market_service

    @staticmethod
    async def get_all_symbol_history() -> List[Dict[str, Dict[str, Any]]]:
        """Fetches historical OHLCV data for all symbols in Redis."""
        symbol_ids = await redis_wrapper.keys()
        histories = []
        for symbol_id in symbol_ids:
            symbol_data = {}
            for key in SYMBOL_HISTORY_KEYS:
                try:
                    symbol_data[key] = redis_wrapper.hget(namespace=symbol_id, key=key)
                except Exception:
                    pass
            histories.append({symbol_id: symbol_data})
        return histories

    def get_stock_watch_info(self, symbol_id: str, limit: int = 10) -> Dict[str, Any]:
        market_depth = self._market_service.get_market_depth(
            symbol_id=symbol_id, limit=limit
        )
        symbol_info = redis_wrapper.hget_symbol_info(symbol_id=symbol_id)
        data = {
            "InstrumentName": symbol_id,
            "CompanyName": symbol_info.base_asset,
            "depth": [],
        }
        for i in range(min(limit, len(market_depth.bids), len(market_depth.asks))):
            level = {
                "bp": market_depth.bids[i][0],
                "bq": market_depth.bids[i][1],
                "ap": market_depth.asks[i][0],
                "aq": market_depth.asks[i][1],
            }
            data["depth"].append(level)
        return data

    def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """Search for symbols in Redis exchangeInfo by partial match."""
        infos = redis_wrapper.hget_all_symbol_info()
        matched_symbols = [symbol for symbol in infos.keys() if query.upper() in symbol]
        results = []
        for symbol_id in matched_symbols:
            info = redis_wrapper.hget_symbol_info(symbol_id=symbol_id)
            results.append(
                dict(
                    symbol_id=symbol_id,
                    kind=info.quote_asset,
                    category=info.base_asset,
                    symbol_name=symbol_id,
                    name=", ".join(info.permissions or []),
                    description="self.CompanyName",  # placeholder
                    title="title",  # placeholder
                )
            )
        return results

    def get_symbol_history(self, symbol_id: str, interval: str) -> Dict[str, Any]:
        """Fetch symbol history for a given interval."""
        data_dict = self.load_history(name=symbol_id, interval=interval)
        df = pd.DataFrame(data=data_dict, index=data_dict["date"])
        df = df.loc[:, SYMBOL_HISTORY_KEYS]

        symbol_info = redis_wrapper.hget_symbol_info(symbol_id=symbol_id)
        return dict(
            per_name=symbol_info.base_asset,
            measurement_name=symbol_info.symbol,
            name=symbol_info.base_asset,
            items=df.to_json(orient="values"),
        )

    @staticmethod
    def get_stock_watch_symbols() -> List[str]:
        """Returns all symbol IDs from the database."""
        return [symbol.symbol_id for symbol in StockWatch.objects.all()]

    def get_all_exchange_symbols(self) -> List[str]:
        """Returns all symbols from Redis exchangeInfo."""
        return [symbol for symbol in redis_wrapper.hget_all_symbol_info()]

    @staticmethod
    def get_user_time_frame(user: User) -> str|None:
        """Returns available intervals and user-specific timeframe."""
        if not user.username:
            return None
        strategy = Strategy.objects.filter(trader=user).first()
        interval = strategy.interval if strategy else "4h"
        return interval
    
    @staticmethod
    def get_intervals() -> list:
        return INTERVALS
    

    def set_history(self, name, interval):
        history_name = self.get_history_name(name, interval)
        params = {
            "symbol": name,
            "interval": interval,
            "limit": settings.CANDLES_HISTORY_LIMIT,
        }
        candles = self._market_service.get_candles(params=params)
        data_dict = {k: [] for k in SYMBOL_HISTORY_KEYS}
        for candle in candles[:-1]:
            for key in SYMBOL_HISTORY_KEYS:
                value = getattr(candle, key)
                data_dict[key].append(value)
        for key, value in data_dict.items():
            redis_wrapper.hset(namespace=history_name, key=key, value=value)


    def get_history_name(self, name, interval):
        return "{}-{}".format(name.upper(), interval)


    def load_history(self, name, interval, num=0):
        if num > 1:
            return {}
        name = name.upper()
        history_name = self.get_history_name(name, interval=interval)
        try:
            dates = redis_wrapper.hget(namespace=history_name, key="date")
            now_ms = UnixMillis.from_dt_to_ms(dt=timezone.now())
            last_candle_time = dates[-1]
            if now_ms - last_candle_time > 2 * INTERVALS[interval]:
                self.set_history(name, interval)
                return self.load_history(name, interval, num=num + 1)
            data_dict = dict()
            for key in SYMBOL_HISTORY_KEYS:
                data_dict[key] = redis_wrapper.hget(namespace=history_name, key=key)
            return data_dict
        except Exception:
            self.set_history(name, interval)
            return self.load_history(name, interval, num=num + 1)
