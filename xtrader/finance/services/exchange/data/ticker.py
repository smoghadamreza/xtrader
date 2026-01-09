from typing import Dict, Any

from dataclasses import dataclass
from finance.services.exchange.constants.binance import BinanceResponseKeys


@dataclass
class Ticker:
    """
    Represents a 24-hour trading summary for a specific cryptocurrency trading pair
    on an exchange like Binance.

    This data comes from the `/api/v3/ticker/24hr` endpoint and provides a snapshot
    of key statistics about price movements, trading volume, and order activity
    over the past 24 hours.

    This is useful for:
    - Displaying summary statistics in trading dashboards or apps
    - Analyzing recent market performance of a trading pair
    - Comparing volatility and activity across assets

    Fields:
    - trading_pair_symbol: Identifier for the asset pair (e.g., BTCUSDT)
    - absolute_price_change: Raw price difference over the last 24 hours
    - percentage_price_change: Price change expressed as a percentage
    - average_traded_price: Volume-weighted average price over the last 24 hours
    - previous_closing_price: Last price before the current 24h window started
    - latest_traded_price: Most recent trade price
    - latest_traded_quantity: Quantity traded in the most recent transaction
    - highest_bid_price: Current highest price someone is willing to buy at
    - highest_bid_quantity: Quantity available at the highest bid
    - lowest_ask_price: Current lowest price someone is willing to sell at
    - lowest_ask_quantity: Quantity available at the lowest ask
    - opening_price: Price at the start of the 24-hour window
    - highest_price_of_day: Highest trade price in the last 24 hours
    - lowest_price_of_day: Lowest trade price in the last 24 hours
    - base_asset_volume: Total amount of the base asset traded (e.g., BTC in BTCUSDT)
    - quote_asset_volume: Total volume in the quote asset (e.g., USDT in BTCUSDT)
    - statistics_open_time: Start timestamp (in milliseconds) of the 24-hour window
    - statistics_close_time: End timestamp (in milliseconds) of the 24-hour window
    - first_trade_id: ID of the first trade in the 24-hour window
    - last_trade_id: ID of the last trade in the 24-hour window
    - total_trade_count: Total number of trades in the last 24 hours
    """
    trading_pair_symbol: str
    absolute_price_change: float
    percentage_price_change: float
    average_traded_price: float
    previous_closing_price: float
    latest_traded_price: float
    latest_traded_quantity: float
    highest_bid_price: float
    highest_bid_quantity: float
    lowest_ask_price: float
    lowest_ask_quantity: float
    opening_price: float
    highest_price_of_day: float
    lowest_price_of_day: float
    base_asset_volume: float
    quote_asset_volume: float
    statistics_open_time: int
    statistics_close_time: int
    first_trade_id: int
    last_trade_id: int
    total_trade_count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ticker":
        return cls(
            trading_pair_symbol=data[BinanceResponseKeys.SYMBOL],
            absolute_price_change=float(data[BinanceResponseKeys.PRICE_CHANGE]),
            percentage_price_change=float(data[BinanceResponseKeys.PRICE_CHANGE_PERCENT]),
            average_traded_price=float(data[BinanceResponseKeys.WEIGHTED_AVG_PRICE]),
            previous_closing_price=float(data[BinanceResponseKeys.PREV_CLOSE_PRICE]),
            latest_traded_price=float(data[BinanceResponseKeys.LAST_PRICE]),
            latest_traded_quantity=float(data[BinanceResponseKeys.LAST_QTY]),
            highest_bid_price=float(data[BinanceResponseKeys.BID_PRICE]),
            highest_bid_quantity=float(data[BinanceResponseKeys.BID_QUANTITY]),
            lowest_ask_price=float(data[BinanceResponseKeys.ASK_PRICE]),
            lowest_ask_quantity=float(data[BinanceResponseKeys.ASK_QUANTITY]),
            opening_price=float(data[BinanceResponseKeys.OPEN_PRICE]),
            highest_price_of_day=float(data[BinanceResponseKeys.HIGH_PRICE]),
            lowest_price_of_day=float(data[BinanceResponseKeys.LOW_PRICE]),
            base_asset_volume=float(data[BinanceResponseKeys.VOLUME]),
            quote_asset_volume=float(data[BinanceResponseKeys.QUOTE_VOLUME]),
            statistics_open_time=int(data[BinanceResponseKeys.OPEN_TIME]),
            statistics_close_time=int(data[BinanceResponseKeys.CLOSE_TIME]),
            first_trade_id=int(data[BinanceResponseKeys.FIRST_TRADE_ID]),
            last_trade_id=int(data[BinanceResponseKeys.LAST_TRADE_ID]),
            total_trade_count=int(data[BinanceResponseKeys.TRADE_COUNT]),
        )
