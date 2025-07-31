from dataclasses import dataclass
from typing import Any, Dict

from finance.exchange.constants.binance import BinanceResponseKeys


@dataclass
class TradeRecord:
    """
    Represents a user's executed trade on Binance.

    Fields:
    - trade_id: Unique identifier of the trade
    - order_id: Associated order ID
    - trading_pair_symbol: Trading pair (e.g. BTCUSDT)
    - execution_price: Trade price
    - base_asset_quantity: Quantity traded
    - quote_asset_quantity: Total cost in quote asset
    - commission_amount: Fee charged
    - commission_asset_symbol: Asset used for the fee
    - execution_time_ms: Trade timestamp in milliseconds
    - was_buyer: Whether the user was the buyer
    - was_maker: Whether the trade was a maker trade
    - was_best_match: Whether this was the best available match
    """

    trade_id: int
    order_id: int
    trading_pair_symbol: str
    execution_price: float
    base_asset_quantity: float
    quote_asset_quantity: float
    commission_amount: float
    commission_asset_symbol: str
    execution_time_ms: int
    was_buyer: bool
    was_maker: bool
    was_best_match: bool

    @classmethod
    def loads(cls, trade: Dict[str, Any]) -> "TradeRecord":
        return cls(
            trade_id=int(trade[BinanceResponseKeys.ID]),
            order_id=int(trade[BinanceResponseKeys.ORDER_ID]),
            trading_pair_symbol=trade[BinanceResponseKeys.SYMBOL],
            execution_price=float(trade[BinanceResponseKeys.PRICE]),
            base_asset_quantity=float(trade[BinanceResponseKeys.QUANTITY]),
            quote_asset_quantity=float(trade[BinanceResponseKeys.QUOTE_QUANTITY]),
            commission_amount=float(trade[BinanceResponseKeys.COMMISSION]),
            commission_asset_symbol=trade[BinanceResponseKeys.COMMISSION_ASSET],
            execution_time_ms=int(trade[BinanceResponseKeys.TIME]),
            was_buyer=trade[BinanceResponseKeys.IS_BUYER],
            was_maker=trade[BinanceResponseKeys.IS_MAKER],
            was_best_match=trade[BinanceResponseKeys.IS_BEST_MATCH]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            BinanceResponseKeys.ID: self.trade_id,
            BinanceResponseKeys.ORDER_ID: self.order_id,
            BinanceResponseKeys.SYMBOL: self.trading_pair_symbol,
            BinanceResponseKeys.PRICE: self.execution_price,
            BinanceResponseKeys.QUANTITY: self.base_asset_quantity,
            BinanceResponseKeys.QUOTE_QUANTITY: self.quote_asset_quantity,
            BinanceResponseKeys.COMMISSION: self.commission_amount,
            BinanceResponseKeys.COMMISSION_ASSET: self.commission_asset_symbol,
            BinanceResponseKeys.TIME: self.execution_time_ms,
            BinanceResponseKeys.IS_BUYER: self.was_buyer,
            BinanceResponseKeys.IS_MAKER: self.was_maker,
            BinanceResponseKeys.IS_BEST_MATCH: self.was_best_match
        }
    

