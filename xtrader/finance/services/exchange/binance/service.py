import requests
import logging
import json
import time
from typing import Dict, Any, List, Union, Final, Optional

from django.conf import settings

from finance.models import Exchange, ExchangeType
from finance.services.exchange.base import BaseExchangeMarketService, BaseExchangeService
from finance.services.exchange.data import (
    DepositRecord, WithdrawalRecord, TransactionRecord,
    SymbolInfo, Candlestick, Ticker, BookTicker, MarketDepth,
    AssetBalance, TradeRecord, AccountSnapshot
)
from .clients import (
    AccountAPIClient, HistoryAPIClient, OrderAPIClient
)
from typing import cast, Dict, List, Any

from data.redis import redis_wrapper as redis
from data.redis.constants import RedisNameSpace, RedisTTL
from finance.services.exchange.constants.binance import BinanceRequestKeys, BinanceResponseKeys
from utils.interval_parser import IntervalParser

logger = logging.getLogger(__name__)



class BinanceService(BaseExchangeService):
    def __init__(self, exchange: Exchange) -> None:
        super().__init__()
        if exchange.type != ExchangeType.BINANCE:
            raise ValueError(f"invalid type {exchange.type} for BinanceExchange")
        self._exchange: Final[Exchange] = exchange
        self._market_service = binance_market_service

        self._account_client = AccountAPIClient(user_exchange=exchange)

        self._history_client = HistoryAPIClient(
            user_exchange=exchange,
            account_api_client=self._account_client
        )
        self._order_client = OrderAPIClient(user_exchange=exchange)

    @property
    def market_service(self) -> BaseExchangeMarketService:
        return self._market_service

    def send_order(self, params: Dict[str, Any]) -> Dict[str, str|bool]:
        return self._order_client.send_order(params=params)

    def cancel_order(self, symbol_id: str, order_id: int) -> Union[Dict[str, Any], List[Any]]:
        return self._order_client.cancel_order(symbol_id=symbol_id, order_id=order_id)

    def cancel_all_orders(self, symbol_id: str) -> Union[Dict[str, Any], List[Any]]:
        return self._order_client.cancel_all_orders(symbol_id=symbol_id)

    def adjust_quantity_to_lot_size(self, symbol_id: str, quantity: float) -> str:
        symbol_info = self.market_service.get_symbol_info(symbol_id=symbol_id)
        return self._order_client.adjust_quantity_to_lot_size(symbol_info=symbol_info, quantity=quantity)

    def get_open_orders(self, symbol_id: str) -> List[Any]:
        return self._account_client.get_open_orders(symbol_id=symbol_id)

    def get_orders(self, symbol_id: str) -> List[Any]:
        return self._account_client.get_orders(symbol_id=symbol_id)

    def get_balance(self) -> int:
        return self._account_client.get_balance()

    def get_portfolio(self) -> List[AssetBalance]:
        return self._account_client.get_portfolio()

    def has_spot_trading_permission(self) -> bool:
        return self._account_client.has_spot_trading_permission()

    def get_recent_nav_snapshots(self) -> List[AccountSnapshot]:
        return self._account_client.get_recent_nav_snapshots()

    def get_deposits(self, params: dict) -> List[DepositRecord]:
        return self._account_client.get_deposits(params=params)

    def get_withdrawals(self, params: dict) -> List[WithdrawalRecord]:
        return self._account_client.get_withdrawals(params=params)

    def get_transactions(self, params: dict) -> List[TransactionRecord]:
        return self._account_client.get_transactions(params=params)

    def get_historical_trades(self, symbol_id: str) -> List[TradeRecord]:
        return self._history_client.get_historical_trades(symbol_id=symbol_id)
    
    def get_historical_deposits(self) -> List[DepositRecord]:
        return self._history_client.get_historical_deposits()

    def get_historical_withdrawals(self) -> List[WithdrawalRecord]:
        return self._history_client.get_historical_withdrawals()

class BinanceMarketService(BaseExchangeMarketService):
    BASE_ASSET_SYMBOL_ID = "USDT"
    FALLBACK_ASSET_SYMBOL_ID  = "BTC"

    BASE_URL = "https://api.binance.com"

    class Endpoint:
        BASE = "/api/v3"
        TICKER = BASE + "/ticker"
        CANDLES = BASE + "/klines"
        TICKER_24HR = TICKER + "/24hr"
        BOOK_TICKER = TICKER + "/bookTicker"
        DEPTH = BASE + "/depth"
        PRICE = TICKER + "/price"
        EXCHANGE_INFO = BASE + "/exchangeInfo"

    class FallBackDataFile:
        ROOT = "finance/services/exchange/binance/fallback_data/"
        EXCHANGE_INFO = ROOT + "exchange_info.json"


    def get_candles(
        self,
        symbol_id: str,
        interval: str,
        limit: int = settings.CANDLES_HISTORY_LIMIT,
        raise_for_status: bool = False,
        use_redis_cache: bool = False
    ) -> List[Candlestick]:
        cache_key = self._get_candle_history_key(
            symbol_id=symbol_id, interval=interval
        )
        candles_data = redis.hget(
            namespace=RedisNameSpace.CANDLES_HISTORY, key=cache_key
        ) if use_redis_cache else None

        if not candles_data:
            candles_data = self._get(
                endpoint=self.Endpoint.CANDLES,
                params={
                    BinanceRequestKeys.SYMBOL: symbol_id,
                    BinanceRequestKeys.INTERVAL: interval,
                    BinanceRequestKeys.LIMIT: limit
                },
                raise_for_status=raise_for_status
            )
            if use_redis_cache:
                redis.hsetex(
                    namespace=RedisNameSpace.CANDLES_HISTORY,
                    key=cache_key,
                    value=candles_data,
                    ttl=IntervalParser.parse_interval_to_seconds(interval=interval)
                )

        return [Candlestick.from_list(c) for c in cast(List[List[float]], candles_data)]


    def get_ticker_24hr(self, symbol_id: str) -> Ticker:  # replaces get_ticker in legacy oms.Binance
        ticker_data = self._get(
            endpoint=self.Endpoint.TICKER_24HR,
            params={
                BinanceRequestKeys.SYMBOL: symbol_id
            }
        )
        ticker_data = cast(Dict[str, Any], ticker_data)
        return Ticker.from_dict(data=ticker_data)
    
    def get_book_ticker(self, symbol_id: str) -> BookTicker:  # replaces get_bookTicker in legacy oms.Binance
        book_ticker_data = self._get(
            endpoint=self.Endpoint.BOOK_TICKER,
            params={
                BinanceRequestKeys.SYMBOL: symbol_id
            }
        )
        book_ticker_data = cast(Dict[str, Any], book_ticker_data)
        return BookTicker.from_dict(data=book_ticker_data)
    
    def get_market_depth(self, symbol_id: str, limit: int) -> MarketDepth:
        data = redis.hget(namespace=RedisNameSpace.MARKET_DEPTH, key=symbol_id)
        if not data:
            data = self._get(
                endpoint=self.Endpoint.DEPTH,
                params={
                    BinanceRequestKeys.SYMBOL: symbol_id,
                    BinanceRequestKeys.LIMIT: limit
                }
            )
            redis.hsetex(
                namespace=RedisNameSpace.MARKET_DEPTH,
                key=symbol_id, value=data,
                ttl=RedisTTL.MARKET_DEPTH
            )
        return MarketDepth.from_dict(
            symbol=symbol_id, data=cast(Dict[str, Any], data)
        )

    def get_last_price(self, symbol_id: str) -> float:
        data = cast(Dict[str, Any], redis.hget(
            namespace=RedisNameSpace.LAST_PRICE,
            key=symbol_id
        ))
        if not data:
            data = cast(Dict[str, Any], self._get(
                endpoint=self.Endpoint.PRICE,
                params={BinanceRequestKeys.SYMBOL: symbol_id}
            )
            )
            redis.hsetex(
                namespace=RedisNameSpace.LAST_PRICE,
                key=symbol_id, value=data,
                ttl=RedisTTL.LAST_PRICE)
        return float(data.get(BinanceResponseKeys.PRICE, 0))


    def get_symbol_info(self, symbol_id: str) -> SymbolInfo:
        data = redis.hget(
            namespace=RedisNameSpace.EXCHANGE_INFO,
            key=symbol_id
        )
        if not data:
            exchange_info_response = self._get(
                endpoint=self.Endpoint.EXCHANGE_INFO,
                params={BinanceRequestKeys.SYMBOL: symbol_id}
            )
            symbols_data: List[Dict[str, Any]] = \
                self._extract_exchange_symbol_info(
                    exchange_info_response=exchange_info_response
                )
            assert len(symbols_data) == 1
            # Store raw Binance dict in Redis
            redis.hsetex(
                namespace=RedisNameSpace.EXCHANGE_INFO,
                key=symbol_id, value=symbols_data[0],
                ttl=RedisTTL.EXCHANGE_INFO
            )
            return SymbolInfo.from_dict(symbols_data[0])
        return SymbolInfo.from_dict(data)

    
    def get_all_symbol_info(self) -> List[SymbolInfo]:
        exchange_info_response = self._get(
            endpoint=self.Endpoint.EXCHANGE_INFO,
            fallback_data_file=self.FallBackDataFile.EXCHANGE_INFO
        )
        symbols_data = self._extract_exchange_symbol_info(
            exchange_info_response=exchange_info_response
        )
        return [SymbolInfo.from_dict(d) for d in symbols_data]


    def get_assets_prices(
        self, assets_symbol_ids: List[str]
    ) -> Dict[str, float]:
        result = {}
        for symbol_id in set(assets_symbol_ids):
            if symbol_id == self.BASE_ASSET_SYMBOL_ID:
                result[symbol_id] = 1.0
                continue
            symbol_pair_id = f"{symbol_id}{self.BASE_ASSET_SYMBOL_ID}"
            price = self.get_last_price(symbol_pair_id)
            if price > 0:
                result[symbol_id] = price
            else:  # fallback via BTC
                fallback_price = self.get_last_price(symbol_pair_id)
                fallback_to_usdt = self.get_last_price(
                    symbol_id=f"{self.FALLBACK_ASSET_SYMBOL_ID}{self.BASE_ASSET_SYMBOL_ID}"
                )
                result[symbol_id] = fallback_price * fallback_to_usdt
        return result

    @staticmethod
    def _extract_exchange_symbol_info(
        exchange_info_response: Any
    ) -> List[Dict[str, Any]]:
        data = cast(Dict[str, Any], exchange_info_response)
        if BinanceResponseKeys.SYMBOLS not in data:
            raise ValueError(f"Missing 'symbols' key in exchange info")
        symbols = cast(List[Dict[str, Any]], data[BinanceResponseKeys.SYMBOLS])
        return [s for s in symbols if s]

    def _get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        raise_for_status: bool = False,
        fallback_data_file: str = "",
        max_retries: int = 3,
        backoff_factor: float = 1.0
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Attempt to GET data from API with retries. Falls back to local JSON file if retries fail.

        :param endpoint: API endpoint
        :param params: Query parameters
        :param raise_for_status: Whether to raise for HTTP errors
        :param fallback_data_file: Path to backup JSON file
        :param max_retries: Maximum retry attempts before fallback
        :param backoff_factor: Multiplier for exponential backoff
        """
        url = self.BASE_URL + endpoint
        attempt = 0

        while attempt < max_retries:
            try:
                logger.info(f"Attempt {attempt+1}/{max_retries}: GET {url} with params={params}")
                response = requests.get(url=url, params=params, timeout=10)

                if raise_for_status:
                    response.raise_for_status()

                logger.info("API request successful")
                return response.json()

            except (requests.RequestException, ValueError) as e:
                attempt += 1
                logger.warning(f"Request attempt {attempt} failed: {e}")

                if attempt < max_retries:
                    sleep_time = backoff_factor * (2 ** (attempt - 1))
                    logger.info(f"Retrying in {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)

        # If all retries failed, try fallback file
        if fallback_data_file:
            try:
                logger.error(f"Max retries reached. Using fallback file: {fallback_data_file}")
                with open(fallback_data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.critical(f"Failed to load fallback file '{fallback_data_file}': {e}")
                raise

        logger.critical("Max retries reached and no fallback file provided.")
        raise RuntimeError("API request failed and no valid fallback available.")
    
    def _get_candle_history_key(self, symbol_id: str, interval: str) -> str:
        return "{symbol_id}-{interval}".format(
            symbol_id=symbol_id,
            interval=interval
        )


binance_market_service = BinanceMarketService()
