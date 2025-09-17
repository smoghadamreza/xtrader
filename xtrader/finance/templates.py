from utils.templates import TemplateFiles


class FinanceTemplates(TemplateFiles):
    """
    Manages template paths for the 'finance' app.
    """
    BASE = "finance/"
    ABOUT_US = BASE + "about_us"
    CONTACT_US = BASE + "contact_us"
    INDEX = BASE + "index"
    MARKET_WATCH_TABLE = BASE + "market_watch_table"
    ORDERS = BASE + "orders"
    SETTINGS = BASE + "settings"
    TEST_API = BASE + "test_api"
    BACK_TEST = BASE + "back_test"
    FARABI = BASE + "farabi"
    MARKET_WATCH = BASE + "market_watch"
    MARTIN_GALE_STRATEGY_RESULTS = BASE + "martin_gale_strategy_results"
    PAYMENT = BASE + "payment"
    STOCK_WATCH = BASE + "stock_watch"
    TEST_VOLUME = BASE + "test_volume"
