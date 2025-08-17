from typing import Dict, Any

from dataclasses import dataclass
from finance.exchange.constants.binance import BinanceResponseKeys


@dataclass
class BookTicker:
    """
    Represents the best current bid (buy) and ask (sell) prices and quantities
    for a given trading pair on a cryptocurrency exchange.

    This class is specifically structured for the Binance `/api/v3/ticker/bookTicker` endpoint,
    which provides the *order book's top level* for each trading pair — that is, the highest price
    someone is willing to buy at (bid), and the lowest price someone is willing to sell at (ask).

    This is useful for:
    - Estimating the real-time spread between buyers and sellers
    - Calculating potential slippage
    - Building bots or tools that track live price dynamics

    Fields:
    - trading_pair_symbol: Identifier for the asset pair being traded (e.g., BTCUSDT)
    - best_bid_price: Highest price at which someone is currently willing to buy
    - best_bid_quantity: Quantity available at the best bid price
    - best_ask_price: Lowest price at which someone is currently willing to sell
    - best_ask_quantity: Quantity available at the best ask price
    """
    trading_pair_symbol: str
    best_bid_price: float
    best_bid_quantity: float
    best_ask_price: float
    best_ask_quantity: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BookTicker":
        return cls(
            trading_pair_symbol=data[BinanceResponseKeys.SYMBOL],
            best_bid_price=float(data[BinanceResponseKeys.BID_PRICE]),
            best_bid_quantity=float(data[BinanceResponseKeys.BID_QUANTITY]),
            best_ask_price=float(data[BinanceResponseKeys.ASK_PRICE]),
            best_ask_quantity=float(data[BinanceResponseKeys.ASK_QUANTITY]),
        )
