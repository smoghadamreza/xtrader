class RedisNameSpace:
    MARKET_DEPTH = "depth"          
    LAST_PRICE = "last_price"       
    EXCHANGE_INFO = "exchange_info"

class RedisTTL:
    """Time-to-live durations (in seconds) for Redis cached data in seconds"""
    MARKET_DEPTH = 5
    LAST_PRICE = 30
    EXCHANGE_INFO = 600  # 10 minutes

SYMBOL_HISTORY_KEYS = ["date", "close_price", "open_price", "high", "low", "volume"]
INTERVALS = [1, 5, 10, 30, 60]