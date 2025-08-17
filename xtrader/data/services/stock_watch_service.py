import json
from typing import List

from data.redis import redis_wrapper
from data.redis.constants import SYMBOL_HISTORY_KEYS, INTERVALS
from data.services.data import SymbolSearchResult, StockWatchInfo
from typing import List, Dict, Any
from django.conf import settings
from django.contrib.auth.models import User
from data.models import StockWatch
from finance.models import Strategy
from finance.exchange.base import BaseExchangeMarketService
from finance.exchange.binance import (
    BinanceMarketService, binance_market_service
)
from finance.exchange.constants.binance import BinanceRequestKeys
from finance.exchange.data import SymbolInfo, Candlestick



class StockWatchService:
    def __init__(self, market_service: BaseExchangeMarketService = BinanceMarketService()) -> None:
        self._market_service = market_service

    @classmethod
    def refresh_symbols_from_binance(cls) -> None:
        """Fetch all tradable symbols from Binance and update Redis set."""
        symbol_infos = binance_market_service.get_all_symbol_info()

        symbols = [info.symbol for info in symbol_infos
            if info.is_symbol_for_trading()]

        redis_wrapper.add_symbols(symbols)

    def get_all_symbol_candles_history(self) -> List[Dict[str, Dict[str, Any]]]:
        # TODO: This function that is being called had no reference to 
        # where it is filling the redis. So according to the keys it expects 
        # in the data, a carefull guess is that it expects CandleSticks.
        # So partly I improvised.
        symbol_ids = redis_wrapper.get_all_symbol_ids()
        candles_histories = []
        for symbol_id in symbol_ids:
            candles = self._market_service.get_candles(
                params={
                    BinanceRequestKeys.SYMBOL: symbol_id,
                    BinanceRequestKeys.INTERVAL: "1m",
                    BinanceRequestKeys.LIMIT: settings.CANDLES_HISTORY_LIMIT,
                },
                use_redis_cache=True
            )
            candles_data = [c.to_dict() for c in candles]
            candles_histories.append({symbol_id: candles_data})
        return candles_histories
    
    def get_symbol_candles_history(self, symbol_id: str, interval: int) -> Dict[str, Any]:
        """Fetch symbol candle history for a given interval."""
        params = {
            BinanceRequestKeys.SYMBOL: symbol_id,
            BinanceRequestKeys.INTERVAL: interval,
            BinanceRequestKeys.LIMIT: settings.CANDLES_HISTORY_LIMIT,
        }
        candles = self._market_service.get_candles(
            params=params,
            use_redis_cache=True
        )
        symbol_info = redis_wrapper.hget_symbol_info(symbol_id=symbol_id)
        return self._prepare_candles_history_payload(
            symbol_info=symbol_info,
            candles=candles
        )
    
    

    def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """Search for symbols in Redis exchangeInfo by partial match."""
        infos_dict = redis_wrapper.hget_all_symbol_info()
        matched_infos = [
            info
            for symbol_id, info in infos_dict.items()
            if query.upper() in symbol_id
        ]

        return [
            SymbolSearchResult.load_from_symbol_info(info=info).to_dict()
            for info in matched_infos
        ]


    def get_stock_watch_info(self, symbol_id: str, limit: int = 10) -> Dict[str, Any]:
        market_depth = self._market_service.get_market_depth(
            symbol_id=symbol_id, limit=limit
        )
        symbol_info = redis_wrapper.hget_symbol_info(symbol_id=symbol_id)
        return StockWatchInfo.load(
            symbol_info=symbol_info,
            market_depth=market_depth
        ).to_dict(depth_limit=limit)

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

    @staticmethod
    def _prepare_candles_history_payload(
        symbol_info: SymbolInfo, candles: List[Candlestick]
    ) -> Dict[str, Any]:
        candles_data = [
            [c_dict[k] for k in SYMBOL_HISTORY_KEYS]
            for c_dict in (c.to_dict() for c in candles)
        ]
        return dict(
            per_name=symbol_info.base_asset,
            measurement_name=symbol_info.symbol,
            name=symbol_info.base_asset,
            items=json.dumps(candles_data),
        )
