from typing import List, Dict, Any, Tuple

from dataclasses import dataclass
from finance.exchange.constants.binance import BinanceResponseKeys


@dataclass
class OrderLevel:
    price: float
    quantity: float


@dataclass
class MarketDepth:
    """
    Represents the current order book depth for a given trading pair on a cryptocurrency exchange.

    This class is structured for the Binance `/api/v3/depth` endpoint, which returns a list of
    price levels for both bids (buy orders) and asks (sell orders), sorted by best price first.

    Unlike the `BookTicker` class which only shows the *top level* of the order book,
    this provides a deeper look into the market’s liquidity by returning multiple levels.

    This is useful for:
    - Understanding the liquidity profile of a trading pair
    - Visualizing the full order book depth
    - Estimating slippage for larger trades
    - Developing advanced trading algorithms and bots

    Fields:
    - trading_pair_symbol: Identifier for the asset pair being traded (e.g., BTCUSDT)
    - last_update_id: Unique ID marking the last update to the order book snapshot
    - bids: List of current buy orders, each as a (price, quantity) tuple; sorted high to low
    - asks: List of current sell orders, each as a (price, quantity) tuple; sorted low to high
    """
    trading_pair_symbol: str
    last_update_id: int
    bids: List[OrderLevel]
    asks: List[OrderLevel]

    @classmethod
    def from_dict(cls, symbol: str, data: Dict[str, Any]) -> "MarketDepth":
        return cls(
            trading_pair_symbol=symbol,
            last_update_id=data[BinanceResponseKeys.LAST_UPDATE_ID],
            bids=[OrderLevel(price=price, quantity=quantity) for price, quantity in data[BinanceResponseKeys.BIDS]],
            asks=[OrderLevel(price=price, quantity=quantity) for price, quantity in data[BinanceResponseKeys.ASKS]],
        )
