from data.apps import DataConfig

class URLMeta(type):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if not name.startswith("__") and isinstance(value, str):
            return DataConfig.name + ":" + value
        return value


class DataURLs(metaclass=URLMeta):
    APP_NAME = DataConfig.name

    GET_SYMBOLS = "get-symbols"
    ALL_SYMBOLS = "all-symbols"
    GET_INTERVALS = "get-intervals"
    ALL_SYMBOLS_HISTORY = "all-symbols-history"
    STOCK_WATCH_INFO = "stock-watch-info"
    SYMBOL_SEARCH = "symbol-search"
    CANDLES_HISTORY = "candles-history"