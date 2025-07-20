from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from .dataclasses import (
    DepositRecord, WithdrawalRecord, SymbolInfo, Candlestick,
    Ticker, BookTicker, MarketDepth, AssetBalance, TradeRecord,
    TransactionRecord
)

class BaseExchangeMarketService(ABC):
    BASE_ASSET_SYMBOL_ID = "USDT"
    FALLBACK_ASSET_SYMBOL_ID  = "BTC"

    @abstractmethod
    def get_candles(self, params: Dict[str, str]) -> List[Candlestick]:
        pass

    @abstractmethod
    def get_ticker_24hr(self, symbol_id: str) -> Ticker:
        pass
    
    @abstractmethod
    def get_book_ticker(self, symbol_id: str) -> BookTicker:
        pass
    
    @abstractmethod
    def get_market_depth(self, symbol_id: str, limit: int) -> MarketDepth:
        pass
    
    @abstractmethod
    def get_last_price(self, symbol_id: str) -> float:
        pass

    @abstractmethod
    def get_symbol_info(self, symbol_id: str) -> SymbolInfo:
        pass
    
    @abstractmethod
    def get_assets_prices(self, assets_symbol_ids: List[str]) -> Dict[str, float]:
        pass


class BaseExchangeService(ABC):

    @property
    def market_service(self) -> BaseExchangeMarketService:
        raise NotImplementedError()

    def get_candles(self, params: Dict[str, Any]) -> List[Candlestick]:
        return self.market_service.get_candles(params=params)

    def get_ticker_24hr(self, symbol_id: str) -> Ticker:
        return self.market_service.get_ticker_24hr(symbol_id=symbol_id)

    def get_book_ticker(self, symbol_id: str) -> BookTicker:
        return self.market_service.get_book_ticker(symbol_id=symbol_id)

    def get_market_depth(self, symbol_id: str, limit: int = 10) -> MarketDepth:
        return self.market_service.get_market_depth(symbol_id=symbol_id, limit=limit)

    def get_symbol_info(self, symbol_id: str) -> SymbolInfo:
        return self.market_service.get_symbol_info(symbol_id=symbol_id)
    
    def get_assets_prices(self, assets_symbol_ids: List[str]) -> Dict[str, float]:
        return self.market_service.get_assets_prices(assets_symbol_ids=assets_symbol_ids)

    def get_last_price(self, symbol_id: str) -> float:
        return self.market_service.get_last_price(symbol_id=symbol_id)

    @abstractmethod
    def send_order(self, params: Dict[str, Any]) -> Dict[str, str|bool]:
        pass

    @abstractmethod
    def cancel_order(self, symbol_id: str, order_id: int) -> Union[Dict[str, Any], List[Any]]:
        pass

    @abstractmethod
    def cancel_all_orders(self, symbol_id: str) -> Union[Dict[str, Any], List[Any]]:
        pass

    @abstractmethod
    def get_open_orders(self, symbol_id: str) -> List[Any]:
        pass

    @abstractmethod
    def get_orders(self, symbol_id: str) -> List[Any]:
        pass

    @abstractmethod
    def get_balance(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_portfolio(self) -> List[AssetBalance]:
        pass

    @abstractmethod
    def has_spot_trading_permission(self) -> bool:
        pass

    @abstractmethod
    def get_recent_nav_snapshots(self) -> List[Dict[str, Any]]:
        pass



    @abstractmethod
    def adjust_quantity_to_lot_size(self, symbol_id: str, quantity: float) -> str:
        pass

    @abstractmethod
    def get_deposits(self, params: dict) -> List[DepositRecord]:
        pass

    @abstractmethod
    def get_withdrawals(self, params: dict) -> List[WithdrawalRecord]:
        pass

    @abstractmethod
    def get_historical_trades(self, symbol_id: str) -> List[TradeRecord]:
        pass

    @abstractmethod
    def get_historical_deposits(self) -> List[DepositRecord]:
        pass

    @abstractmethod
    def get_historical_withdrawals(self) -> List[WithdrawalRecord]:
        pass

    @abstractmethod
    def get_transactions(self, params: dict) -> List[TransactionRecord]:
        pass
