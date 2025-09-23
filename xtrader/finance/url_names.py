from finance.apps import FinanceConfig

class URLMeta(type):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if not name.startswith("__") and isinstance(value, str):
            return FinanceConfig.name + ":" + value
        return value

class FinanceURLS(metaclass=URLMeta):
    APP_NAME = FinanceConfig.name

    SETTINGS = "settings"
    SETTINGS_EXCHANGE = SETTINGS + "/?s=exchange"
    SETTINGS_TELEGRAM = SETTINGS + "/?s=telegram"
    SETTINGS_TRADINGVIEW = SETTINGS + "/?s=tradingView"
    SETTINGS_WATCHLIST = SETTINGS + "/?s=watchlist"
    SETTINGS_PACKAGES = SETTINGS + "/?s=packages"
    SETTINGS_WALLET = SETTINGS + "/?s=wallet"
    SETTINGS_PROMOTE = SETTINGS + "/?s=promote"
