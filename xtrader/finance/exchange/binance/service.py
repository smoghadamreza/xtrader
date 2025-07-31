import requests
from typing import Dict, Any, List, Union, Final, Optional

from finance.models import Exchange, ExchangeType
from finance.exchange.base import BaseExchangeMarketService, BaseExchangeService
from finance.exchange.data import (
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
from finance.exchange.constants.binance import BinanceRequestKeys, BinanceResponseKeys


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



    def get_candles(self, params: Dict[str, str]) -> List[Candlestick]:
        candles_data = self._get(
            endpoint=self.Endpoint.CANDLES,
            params=params
        )
        candles_data = cast(List[List[float|int]], candles_data)
        return [Candlestick.from_list(c) for c in candles_data]

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
    
    def get_market_depth(self, symbol_id: str, limit: int) -> MarketDepth:  # replaces get_depth in legacy oms.Binance
        market_depth_data =  redis.hget(
            namespace=RedisNameSpace.MARKET_DEPTH,
            key=symbol_id
        )
        if market_depth_data is None:
            market_depth_data = self._get(
                endpoint=self.Endpoint.DEPTH,
                params={
                    BinanceRequestKeys.SYMBOL: symbol_id, BinanceRequestKeys.LIMIT: limit
                }
            )
            market_depth_data = cast(Dict[str, Any], market_depth_data)
            redis.hsetex(
                namespace=RedisNameSpace.MARKET_DEPTH,
                key=symbol_id,
                value=market_depth_data,
                ttl=RedisTTL.MARKET_DEPTH
            )
        return MarketDepth.from_dict(symbol=symbol_id, data=market_depth_data)
    
    def get_last_price(self, symbol_id: str) -> float:
        last_price_data =  redis.hget(
            namespace=RedisNameSpace.LAST_PRICE,
            key=symbol_id
        )
        if last_price_data is None:
            last_price_data = self._get(
                endpoint=self.Endpoint.PRICE,
                params={
                    BinanceRequestKeys.SYMBOL: symbol_id
                }
            )
            last_price_data = cast(Dict[str, Any], last_price_data)
            redis.hsetex(
                namespace=RedisNameSpace.LAST_PRICE,
                key=symbol_id,
                value=float(last_price_data[BinanceResponseKeys.PRICE]),
                ttl=RedisTTL.LAST_PRICE
            )

        return last_price_data.get(BinanceResponseKeys.PRICE, 0)

    def get_symbol_info(self, symbol_id: str) -> SymbolInfo:  # Make sure the symbol_id is only in upper case.
        exchange_symbol_info_data = redis.hget(
            namespace=RedisNameSpace.EXCHANGE_INFO,
            key=symbol_id
        )
        if exchange_symbol_info_data is None: 
            exchange_info_response = self._get(
                endpoint=self.Endpoint.EXCHANGE_INFO,
                params={BinanceRequestKeys.SYMBOL: symbol_id}
            )
            exchange_symbol_info_data = self._extract_exchange_symbol_info_data(
                exchange_info_response=exchange_info_response
            )
            redis.hsetex(
                namespace=RedisNameSpace.EXCHANGE_INFO,
                key=symbol_id,
                value=exchange_symbol_info_data,
                ttl=RedisTTL.EXCHANGE_INFO
            )
        return SymbolInfo.from_dict(data=exchange_symbol_info_data)
    
    def get_assets_prices(self, assets_symbol_ids: List[str]) -> Dict[str, float]:  # Replaces get_prices_for_nav in legacy Binance.get_prices_for_nav
        """Get prices for Net Asset Value (NAV) calculation with fallback mechanism"""
        result = {}
        unique_symbol_ids = list(set(assets_symbol_ids))
        for symbol_id in unique_symbol_ids:
            if symbol_id == self.BASE_ASSET_SYMBOL_ID:
                result[self.BASE_ASSET_SYMBOL_ID] = 1.0
                continue
                
            symbol_pair_id = f"{symbol_id}{self.BASE_ASSET_SYMBOL_ID}"
            price = self.get_last_price(symbol_id=symbol_pair_id)
            
            if price > 0:
                result[symbol_id] = price
            else:  # Fallback
                fallback_asset_price = self.get_last_price(
                    symbol_id=f"{symbol_id}{self.BASE_ASSET_SYMBOL_ID}"
                )

                fallback_asset_to_usdt_price = self.get_last_price(
                    symbol_id=f"{self.FALLBACK_ASSET_SYMBOL_ID}{self.BASE_ASSET_SYMBOL_ID}"
                )
                result[symbol_id] = fallback_asset_price * fallback_asset_to_usdt_price
        return result

    @staticmethod
    def _extract_exchange_symbol_info_data(exchange_info_response: Any) -> Dict[str, Any]:
        data = cast(Dict[str, Any], exchange_info_response)
        if BinanceResponseKeys.SYMBOLS not in data:
            raise ValueError(f"the required key 'symbols' is not present in exchange_info")
        data = data[BinanceResponseKeys.SYMBOLS]
        data = cast(List[Any], data)
        if not data or len(data) != 1:
            raise ValueError(f"Unexpected symbol info response: {data}")

        data = data[0]
        data = cast( Dict[str, Any], data)
        return data
    
    def _get(self, endpoint: str, params: Optional[dict] = None) -> Union[Dict[str, Any], List[Any]]:
        response = requests.get(
            url=self.BASE_URL + endpoint,
            params=params
        )
        return response.json()

binance_market_service = BinanceMarketService()
