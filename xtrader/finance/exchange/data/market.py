from typing import List, Union, Dict, Any, Tuple

from dataclasses import dataclass
from finance.exchange.constants.binance import BinanceResponseKeys, BinanceResponseValues

@dataclass
class Candlestick:
    """
    Represents a single candlestick (or "kline") for a specific time interval on a
    cryptocurrency trading pair.

    Candlesticks are used in trading charts to show how price and volume have changed
    during a fixed period (e.g., 1 minute, 1 hour, 1 day). Each candlestick contains
    the opening and closing prices, as well as the high and low during the interval.

    This class corresponds to Binance's `/api/v3/klines` endpoint, which returns a
    list of such candlesticks in array form.

    This is useful for:
    - Visualizing historical price movement
    - Building price charts (e.g., OHLC or candlestick charts)
    - Performing technical analysis or backtesting

    Fields:
    - open_time: Start timestamp (in milliseconds) of the candlestick interval
    - open_price: Price at the beginning of the interval
    - high: Highest price during the interval
    - low: Lowest price during the interval
    - close_price: Price at the end of the interval
    - volume: Amount of the base asset traded during the interval
    - close_time: End timestamp (in milliseconds) of the candlestick interval
    - quote_volume: Total value traded in terms of the quote asset
    - number_of_trades: Total number of trades that occurred during the interval
    - taker_buy_base_volume: Volume of base asset bought by "takers" (market buyers)
    - taker_buy_quote_volume: Corresponding quote asset volume of taker buys
    - ignore: Placeholder field (usually 0 or unused string — safe to ignore)
    """
    open_time: int
    open_price: float
    high: float
    low: float
    close_price: float
    volume: float
    close_time: int
    quote_volume: float
    number_of_trades: int
    taker_buy_base_volume: float
    taker_buy_quote_volume: float
    ignore: Union[int, str]

    @classmethod
    def from_list(cls, data: List[float | int]) -> "Candlestick":
        return cls(
            open_time=int(data[0]),
            open_price=float(data[1]),
            high=float(data[2]),
            low=float(data[3]),
            close_price=float(data[4]),
            volume=float(data[5]),
            close_time=int(data[6]),
            quote_volume=float(data[7]),
            number_of_trades=int(data[8]),
            taker_buy_base_volume=float(data[9]),
            taker_buy_quote_volume=float(data[10]),
            ignore=str(data[11])
        )
    

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
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]

    @classmethod
    def from_dict(cls, symbol: str, data: Dict[str, Any]) -> "MarketDepth":
        return cls(
            trading_pair_symbol=symbol,
            last_update_id=data[BinanceResponseKeys.LAST_UPDATE_ID],
            bids=[(float(price), float(quantity)) for price, quantity in data[BinanceResponseKeys.BIDS]],
            asks=[(float(price), float(quantity)) for price, quantity in data[BinanceResponseKeys.ASKS]],
        )

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LotFilter:
    """
    Represents a LOT_SIZE filter from Binance exchange info.

    Fields:
    - filter_type: Should always be "LOT_SIZE"
    - min_quantity: Minimum quantity allowed per order
    - max_quantity: Maximum quantity allowed per order
    - step_size: Step size for quantity increments
    """
    filter_type: str
    min_quantity: float
    max_quantity: float
    step_size: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LotFilter":
        return cls(
            filter_type=data[BinanceResponseKeys.FILTER_TYPE],
            min_quantity=float(data[BinanceResponseKeys.MIN_QUANTITY]),
            max_quantity=float(data[BinanceResponseKeys.MAX_QUANTITY]),
            step_size=float(data[BinanceResponseKeys.STEP_SIZE]),
        )


@dataclass
class SymbolInfo:
    """
    Represents metadata for a trading symbol on Binance.

    Fields:
    - symbol: Trading symbol (e.g., BTCUSDT)
    - status: Trading status
    - base_asset, quote_asset: Base and quote asset symbols
    - precision fields: Decimal precision for trading/commission
    - supported_order_types: Allowed order types
    - boolean flags for feature support
    - lot_filter: Only the single LOT_SIZE filter
    - permissions, STP modes: Various optional config details
    """

    symbol: str
    status: str
    base_asset: str
    base_asset_precision: int
    quote_asset: str
    quote_precision: int
    quote_asset_precision: int
    base_commission_precision: int
    quote_commission_precision: int
    supported_order_types: List[str]
    is_iceberg_order_allowed: bool
    is_one_cancels_other_allowed: bool
    is_one_triggers_other_allowed: bool
    is_quote_quantity_market_order_allowed: bool
    is_trailing_stop_order_allowed: bool
    is_cancel_replace_allowed: bool
    is_order_amend_allowed: bool
    is_spot_trading_allowed: bool
    is_margin_trading_allowed: bool
    lot_filter: Optional[LotFilter]
    permissions: Optional[List[str]]
    permission_sets: Optional[List[List[str]]]
    default_self_trade_prevention_mode: Optional[str]
    allowed_self_trade_prevention_modes: Optional[List[str]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SymbolInfo":
        lot_filter = next(
            (
                LotFilter.from_dict(f)
                for f in data.get(BinanceResponseKeys.FILTERS, [])
                if f.get(BinanceResponseKeys.FILTER_TYPE) == BinanceResponseValues.LOT_SIZE
            ),
            None
        )


        return cls(
            symbol=data[BinanceResponseKeys.SYMBOL],
            status=data[BinanceResponseKeys.STATUS],
            base_asset=data[BinanceResponseKeys.BASE_ASSET],
            base_asset_precision=data[BinanceResponseKeys.BASE_ASSET_PRECISION],
            quote_asset=data[BinanceResponseKeys.QUOTE_ASSET],
            quote_precision=data[BinanceResponseKeys.QUOTE_PRECISION],
            quote_asset_precision=data[BinanceResponseKeys.QUOTE_ASSET_PRECISION],
            base_commission_precision=data[BinanceResponseKeys.BASE_COMMISSION_PRECISION],
            quote_commission_precision=data[BinanceResponseKeys.QUOTE_COMMISSION_PRECISION],
            supported_order_types=data[BinanceResponseKeys.ORDER_TYPES],
            is_iceberg_order_allowed=data[BinanceResponseKeys.ICEBERG_ALLOWED],
            is_one_cancels_other_allowed=data[BinanceResponseKeys.OCO_ALLOWED],
            is_one_triggers_other_allowed=data[BinanceResponseKeys.OTO_ALLOWED],
            is_quote_quantity_market_order_allowed=data[BinanceResponseKeys.QUOTE_ORDER_QTY_MARKET_ALLOWED],
            is_trailing_stop_order_allowed=data[BinanceResponseKeys.ALLOW_TRAILING_STOP],
            is_cancel_replace_allowed=data[BinanceResponseKeys.CANCEL_REPLACE_ALLOWED],
            is_order_amend_allowed=data[BinanceResponseKeys.AMEND_ALLOWED],
            is_spot_trading_allowed=data[BinanceResponseKeys.IS_SPOT_TRADING_ALLOWED],
            is_margin_trading_allowed=data[BinanceResponseKeys.IS_MARGIN_TRADING_ALLOWED],
            lot_filter=lot_filter,
            permissions=data.get(BinanceResponseKeys.PERMISSIONS),
            permission_sets=data.get(BinanceResponseKeys.PERMISSION_SETS),
            default_self_trade_prevention_mode=data.get(BinanceResponseKeys.DEFAULT_STP_MODE),
            allowed_self_trade_prevention_modes=data.get(BinanceResponseKeys.ALLOWED_STP_MODES),
        )
