# TODO: For now dataclasses in this file only represent Binance related data. 
# When you want to add another exchange to the project, make sure to 
# create proper parent class to use in AbstractExchangeService
# response types.

from typing import cast, List, Union, Dict, Any, Type

from dataclasses import dataclass
from .consts import ResponseKeys, LOT_SIZE

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
    - open: Price at the beginning of the interval
    - high: Highest price during the interval
    - low: Lowest price during the interval
    - close: Price at the end of the interval
    - volume: Amount of the base asset traded during the interval
    - close_time: End timestamp (in milliseconds) of the candlestick interval
    - quote_volume: Total value traded in terms of the quote asset
    - number_of_trades: Total number of trades that occurred during the interval
    - taker_buy_base_volume: Volume of base asset bought by "takers" (market buyers)
    - taker_buy_quote_volume: Corresponding quote asset volume of taker buys
    - ignore: Placeholder field (usually 0 or unused string — safe to ignore)
    """
    open_time: int
    open: float
    high: float
    low: float
    close: float
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
            open=float(data[1]),
            high=float(data[2]),
            low=float(data[3]),
            close=float(data[4]),
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
            trading_pair_symbol=data[ResponseKeys.SYMBOL],
            absolute_price_change=float(data[ResponseKeys.PRICE_CHANGE]),
            percentage_price_change=float(data[ResponseKeys.PRICE_CHANGE_PERCENT]),
            average_traded_price=float(data[ResponseKeys.WEIGHTED_AVG_PRICE]),
            previous_closing_price=float(data[ResponseKeys.PREV_CLOSE_PRICE]),
            latest_traded_price=float(data[ResponseKeys.LAST_PRICE]),
            latest_traded_quantity=float(data[ResponseKeys.LAST_QTY]),
            highest_bid_price=float(data[ResponseKeys.BID_PRICE]),
            highest_bid_quantity=float(data[ResponseKeys.BID_QUANTITY]),
            lowest_ask_price=float(data[ResponseKeys.ASK_PRICE]),
            lowest_ask_quantity=float(data[ResponseKeys.ASK_QUANTITY]),
            opening_price=float(data[ResponseKeys.OPEN_PRICE]),
            highest_price_of_day=float(data[ResponseKeys.HIGH_PRICE]),
            lowest_price_of_day=float(data[ResponseKeys.LOW_PRICE]),
            base_asset_volume=float(data[ResponseKeys.VOLUME]),
            quote_asset_volume=float(data[ResponseKeys.QUOTE_VOLUME]),
            statistics_open_time=int(data[ResponseKeys.OPEN_TIME]),
            statistics_close_time=int(data[ResponseKeys.CLOSE_TIME]),
            first_trade_id=int(data[ResponseKeys.FIRST_TRADE_ID]),
            last_trade_id=int(data[ResponseKeys.LAST_TRADE_ID]),
            total_trade_count=int(data[ResponseKeys.TRADE_COUNT]),
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
            trading_pair_symbol=data[ResponseKeys.SYMBOL],
            best_bid_price=float(data[ResponseKeys.BID_PRICE]),
            best_bid_quantity=float(data[ResponseKeys.BID_QUANTITY]),
            best_ask_price=float(data[ResponseKeys.ASK_PRICE]),
            best_ask_quantity=float(data[ResponseKeys.ASK_QUANTITY]),
        )

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any


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
            last_update_id=data[ResponseKeys.LAST_UPDATE_ID],
            bids=[(float(price), float(quantity)) for price, quantity in data[ResponseKeys.BIDS]],
            asks=[(float(price), float(quantity)) for price, quantity in data[ResponseKeys.ASKS]],
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
            filter_type=data[ResponseKeys.FILTER_TYPE],
            min_quantity=float(data[ResponseKeys.MIN_QUANTITY]),
            max_quantity=float(data[ResponseKeys.MAX_QUANTITY]),
            step_size=float(data[ResponseKeys.STEP_SIZE]),
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
                for f in data.get(ResponseKeys.FILTERS, [])
                if f.get(ResponseKeys.FILTER_TYPE) == LOT_SIZE
            ),
            None
        )


        return cls(
            symbol=data[ResponseKeys.SYMBOL],
            status=data[ResponseKeys.STATUS],
            base_asset=data[ResponseKeys.BASE_ASSET],
            base_asset_precision=data[ResponseKeys.BASE_ASSET_PRECISION],
            quote_asset=data[ResponseKeys.QUOTE_ASSET],
            quote_precision=data[ResponseKeys.QUOTE_PRECISION],
            quote_asset_precision=data[ResponseKeys.QUOTE_ASSET_PRECISION],
            base_commission_precision=data[ResponseKeys.BASE_COMMISSION_PRECISION],
            quote_commission_precision=data[ResponseKeys.QUOTE_COMMISSION_PRECISION],
            supported_order_types=data[ResponseKeys.ORDER_TYPES],
            is_iceberg_order_allowed=data[ResponseKeys.ICEBERG_ALLOWED],
            is_one_cancels_other_allowed=data[ResponseKeys.OCO_ALLOWED],
            is_one_triggers_other_allowed=data[ResponseKeys.OTO_ALLOWED],
            is_quote_quantity_market_order_allowed=data[ResponseKeys.QUOTE_ORDER_QTY_MARKET_ALLOWED],
            is_trailing_stop_order_allowed=data[ResponseKeys.ALLOW_TRAILING_STOP],
            is_cancel_replace_allowed=data[ResponseKeys.CANCEL_REPLACE_ALLOWED],
            is_order_amend_allowed=data[ResponseKeys.AMEND_ALLOWED],
            is_spot_trading_allowed=data[ResponseKeys.IS_SPOT_TRADING_ALLOWED],
            is_margin_trading_allowed=data[ResponseKeys.IS_MARGIN_TRADING_ALLOWED],
            lot_filter=lot_filter,
            permissions=data.get(ResponseKeys.PERMISSIONS),
            permission_sets=data.get(ResponseKeys.PERMISSION_SETS),
            default_self_trade_prevention_mode=data.get(ResponseKeys.DEFAULT_STP_MODE),
            allowed_self_trade_prevention_modes=data.get(ResponseKeys.ALLOWED_STP_MODES),
        )

@dataclass
class AssetBalance:
    """
    Represents the available and locked balance of an asset in a Binance wallet.

    Fields:
    - symbol: The asset symbol (e.g., BTC, ETH)
    - free: Amount of the asset freely available for trading
    - locked: Amount of the asset currently locked (e.g., in orders)

    This is useful for:
    - Displaying user wallet status
    - Validating sufficient balance before placing trades
    - Monitoring changes in balance after trade execution
    """

    symbol: str
    free: float
    locked: float

    @classmethod
    def loads(cls, balance: Dict[str, Any]) -> "AssetBalance":
        return cls(
            symbol=balance[ResponseKeys.ASSET],
            free=float(balance[ResponseKeys.FREE]),
            locked=float(balance[ResponseKeys.LOCKED])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            ResponseKeys.SYMBOL: self.symbol,
            ResponseKeys.FREE: self.free,
            ResponseKeys.LOCKED: self.locked
        }

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
            trade_id=int(trade[ResponseKeys.ID]),
            order_id=int(trade[ResponseKeys.ORDER_ID]),
            trading_pair_symbol=trade[ResponseKeys.SYMBOL],
            execution_price=float(trade[ResponseKeys.PRICE]),
            base_asset_quantity=float(trade[ResponseKeys.QUANTITY]),
            quote_asset_quantity=float(trade[ResponseKeys.QUOTE_QUANTITY]),
            commission_amount=float(trade[ResponseKeys.COMMISSION]),
            commission_asset_symbol=trade[ResponseKeys.COMMISSION_ASSET],
            execution_time_ms=int(trade[ResponseKeys.TIME]),
            was_buyer=trade[ResponseKeys.IS_BUYER],
            was_maker=trade[ResponseKeys.IS_MAKER],
            was_best_match=trade[ResponseKeys.IS_BEST_MATCH]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            ResponseKeys.ID: self.trade_id,
            ResponseKeys.ORDER_ID: self.order_id,
            ResponseKeys.SYMBOL: self.trading_pair_symbol,
            ResponseKeys.PRICE: self.execution_price,
            ResponseKeys.QUANTITY: self.base_asset_quantity,
            ResponseKeys.QUOTE_QUANTITY: self.quote_asset_quantity,
            ResponseKeys.COMMISSION: self.commission_amount,
            ResponseKeys.COMMISSION_ASSET: self.commission_asset_symbol,
            ResponseKeys.TIME: self.execution_time_ms,
            ResponseKeys.IS_BUYER: self.was_buyer,
            ResponseKeys.IS_MAKER: self.was_maker,
            ResponseKeys.IS_BEST_MATCH: self.was_best_match
        }
    
@dataclass
class DepositRecord:
    """
    Represents a deposit record from Binance deposit history endpoint.

    Fields:
    - deposit_id: Unique identifier for the deposit
    - asset_symbol: The asset symbol deposited (e.g., BTC, USDT)
    - deposit_amount: The amount deposited
    - deposit_address: The address to which deposit was sent
    - transaction_id: Blockchain transaction ID for the deposit
    - deposit_status: Status code of the deposit
    - insert_time_ms: Time the deposit was inserted (timestamp in milliseconds)
    - confirm_times: Number of confirmations required
    - address_tag: Optional address tag or memo (if applicable)
    """

    deposit_id: int
    asset_symbol: str
    deposit_amount: float
    deposit_address: str
    transaction_id: str
    deposit_status: int
    insert_time_ms: int
    confirm_times: str
    address_tag: str

    @classmethod
    def loads(cls, deposit: Dict[str, Any]) -> "DepositRecord":
        return cls(
            deposit_id=int(deposit[ResponseKeys.ID]),
            asset_symbol=deposit[ResponseKeys.ASSET],
            deposit_amount=float(deposit[ResponseKeys.AMOUNT]),
            deposit_address=deposit[ResponseKeys.ADDRESS],
            transaction_id=deposit[ResponseKeys.TRANSACTION_ID],
            deposit_status=int(deposit[ResponseKeys.STATUS]),
            insert_time_ms=int(deposit[ResponseKeys.INSERT_TIME]),
            confirm_times=deposit[ResponseKeys.CONFIRM_TIMES],
            address_tag=deposit.get(ResponseKeys.ADDRESS_TAG, "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            ResponseKeys.ID: self.deposit_id,
            ResponseKeys.ASSET: self.asset_symbol,
            ResponseKeys.AMOUNT: self.deposit_amount,
            ResponseKeys.ADDRESS: self.deposit_address,
            ResponseKeys.TRANSACTION_ID: self.transaction_id,
            ResponseKeys.STATUS: self.deposit_status,
            ResponseKeys.INSERT_TIME: self.insert_time_ms,
            ResponseKeys.CONFIRM_TIMES: self.confirm_times,
            ResponseKeys.ADDRESS_TAG: self.address_tag,
        }

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class WithdrawalRecord:
    """
    Represents a withdrawal record from Binance withdrawal history endpoint.

    Fields:
    - withdrawal_id: Unique identifier for the withdrawal
    - asset_symbol: The asset symbol withdrawn (e.g., BTC, USDT)
    - withdrawal_amount: The amount withdrawn
    - transaction_fee: The fee charged for the withdrawal
    - withdrawal_address: The address the funds were sent to
    - network: Blockchain network used for withdrawal
    - transaction_id: Blockchain transaction ID
    - withdrawal_status: Status code of the withdrawal
    - apply_time_str: Timestamp as string when the withdrawal was requested
    - transfer_type: Indicates internal transfer (0 = external, 1 = internal)
    """

    withdrawal_id: str
    asset_symbol: str
    withdrawal_amount: float
    transaction_fee: float
    withdrawal_address: str
    network: str
    transaction_id: str
    withdrawal_status: int
    apply_time_ms: int
    transfer_type: int

    @classmethod
    def loads(cls, withdrawal: Dict[str, Any]) -> "WithdrawalRecord":
        return cls(
            withdrawal_id=withdrawal[ResponseKeys.ID],
            asset_symbol=withdrawal[ResponseKeys.COIN],
            withdrawal_amount=float(withdrawal[ResponseKeys.AMOUNT]),
            transaction_fee=float(withdrawal[ResponseKeys.TRANSACTION_FEE]),
            withdrawal_address=withdrawal[ResponseKeys.ADDRESS],
            network=withdrawal[ResponseKeys.NETWORK],
            transaction_id=withdrawal[ResponseKeys.TRANSACTION_ID],
            withdrawal_status=int(withdrawal[ResponseKeys.STATUS]),
            apply_time_ms=withdrawal[ResponseKeys.APPLY_TIME],
            transfer_type=int(withdrawal[ResponseKeys.TRANSFER_TYPE]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            ResponseKeys.ID: self.withdrawal_id,
            ResponseKeys.COIN: self.asset_symbol,
            ResponseKeys.AMOUNT: self.withdrawal_amount,
            ResponseKeys.TRANSACTION_FEE: self.transaction_fee,
            ResponseKeys.ADDRESS: self.withdrawal_address,
            ResponseKeys.NETWORK: self.network,
            ResponseKeys.TRANSACTION_ID: self.transaction_id,
            ResponseKeys.STATUS: self.withdrawal_status,
            ResponseKeys.APPLY_TIME: self.apply_time_ms,
            ResponseKeys.TRANSFER_TYPE: self.transfer_type,
        }

@dataclass
class TransactionRecord:
    record_type: Type[Union[DepositRecord, WithdrawalRecord]]
    amount: float
    time: int
    metadata: Union[DepositRecord, WithdrawalRecord]

    @classmethod
    def loads(cls, record: Union[DepositRecord, WithdrawalRecord]) -> "TransactionRecord":
        if hasattr(record, "insert_time_ms"):
            deposit = cast(DepositRecord, record)
            return cls(
                record_type=DepositRecord,
                amount=deposit.deposit_amount,
                time=deposit.insert_time_ms,
                metadata=deposit
            )
        elif hasattr(record, "apply_time_ms"):
            # Convert string timestamp to milliseconds if needed
            withdrawal = cast(WithdrawalRecord, record)
            return cls(
                record_type=WithdrawalRecord,
                amount=withdrawal.withdrawal_amount,
                time=withdrawal.apply_time_ms,
                metadata=withdrawal
            )
        else:
            raise TypeError("Unsupported record type for TransactionRecord")

