from typing import List, Union
from dataclasses import dataclass, asdict

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
    
    def to_dict(self):
        return asdict(self)
