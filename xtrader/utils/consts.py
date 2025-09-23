class RequestType:
    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"

class Symbol:
    USDT = "USDT"
    BTCUSDT = "BTCUSDT"

class XtraderRequestKeys:
    # Multiple Usage
    ACTION = "action"
    NAME = "name"
    WATCHLIST_ID = "watchListId"

    # used in aum.views
    INVESTOR_ID = "investor_id"
    AMOUNT = "amount"
    PASS = "pass"
    MODE = "mode"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    NATIONAL_CODE = "nationalCode"

    # used in account.views
    NONCE = "nonce"
    USERNAME = "username"

    # Used in finance/views/tradingview_views.py
    MESSAGE = "message"
    FROM = "from"
    ID = "id"
    TEXT = "text"

    # Used in finance/views/watchlist_views.py
    SYMBOL = "symbol"

    # Used in finance/services/strategy_services.py
    FILTERS = "filters"
    INTERVAL = "interval"

    # Used in finance/views/strategy_views.py
    SYMBOL_ID = "symbol_id"
    PARAM = "param"
    STRATEGY_ID = "strategyId"
    TRADES = "trades"
    CONFIG = "config"


    # Used in finance/services/indicators/indicator_service.py
    INDICATOR_TYPE = "kind"

    REFERRAL_CODE = "ref"
    ORDER = "order"

    # Used in finance/views/market_views.py
    PAGE = "page"
    

class XtraderRequestValues:
    # used in finance.copy_trade
    NEW = "NEW"
    CANCEL = "CANCELED"

    # used in aum.FundService.issue_redeem_unit
    ISSUE = "issue"
    REDEEM = "redeem"

    # used in aum.views
    XTREASURY = "XTreasury"
    ALL = "all"
    FUND = "fund"
    BTC = "btc"

    # used in finanice/views/tradingview_views.py
    START = "/start"
    ADD = "add"
    REMOVE = "remove"
    BTC_USDT = "BTCUSDT"
    DEFAULT_WATCHLIST_ID = "0"

    class Interval:
        ONE_HOUR = "1h"
        ONE_DAY = "1d"


class XtraderResponseKeys:
    C = "c"  # TODO: I think this supposed to be status code.
    M = "m"  # TODO: I think this supposed to be message.
    S = "s"  # TODO: I think this supposed to be status code.
    MESSAGE = "msg"
    DATA = "data"
    ID = "id"
    STATUS = "status"
    TELEGRAM = "telegram"


    # used in data.views
    INTERVALS = "intervals"
    USER_TIME_FRAME = "userTimeFrame"
    SYMBOLS = "symbols"
    TITLE = "title"
    ITEMS = "items"

    # used in accounts.views
    FOLLOWING = "following"
    EXCHANGE = "exchange"
    PRO_TRADER = "protrader"
    NEW_DEPOSIT = "newDeposit"
    TELEGRAM_ID = "telegram_id"
    ACTIVATION_CODE = "activation_code"

    # Used in accounts/views/wallet_views.py
    FAILED_COUNT = "failed_count"

    # Used in finance/views/tradingview_views.py
    ORDER = "order"
    ERROR = "error"
    RAMZ_E_SERVAT = "Ramzservat"
    WEBHOOK = "webhook"
    TRADING = "trading"
    NOTIFICATION = "notification"

    # Used in finance/views/watchlist_views.py
    REDIRECT = "redirect"
    TYPE = "type"
    WATCHLISTS = "watchlists"
    
    NAME = "name"
    IMAGE_URL = "img_url"

    SYMBOL_ID = "SymbolId"
    EXCHANGES = "exchanges"
    ORDERS = "orders"
    ASSETS = "assets"

    # Used in finance/views/market_views.py
    STOCKS = "stocks"
    LAST_PAGE = "last"
    SUBSCRIBES = "subscribes"

    # Used in finance/views/strategy_views.py
    STRATEGIES = "strategies"

class XtraderResponseMessages:
    # Used in accounts/views/authentication_views.py
    ACTIVATION_LINK_INVALID = "لینک فعال‌سازی نامعتبر است."
    ACTIVATION_LINK_EXPIRED_RETRY = "لینک فعال‌سازی منقضی شده است، لطفا دوباره تلاش کنید."
    ACTIVATION_LINK_NOT_EXPIRED = "لینک فعال‌سازی منقضی نشده است!"
    EMAIL_CHANGE_SUCCESS = "آدرس ایمیل شما با موفقیت تغییر یافت."
    SIGNIN_SUCCESS = "شما با موفقیت وارد شدید."
    SIGNOUT_SUCCESS = "شما با موفقیت خارج شدید."
    USERNAME_NOT_FOUND = "نام کاربری وارد شده وجود ندارد!"
    INCORRECT_PASSWORD = "گذرواژه اشتباه است!"

    # Used in accounts/views/profile_views.py
    PROFILE_IS_UPDATED = "حساب کاربری شما به‌روزرسانی شد."

    # Used in accounts/views/wallet_views.py
    NO_PROFILE_FOR_USER = "خطای غیر منتظره! کاربر شما حساب کاربری ندارد. با پشتیبانی تماس بگیرید."
    NO_WALLET_FOR_USER = "کیف پولی به حساب شما متصل نیست."

    # Used in finance/views/tradingview_views.py
    SOMETHING_WENT_WRONG = "مشکلی پیش آمده است."
    ACTION_SUCCESS = "عملیات درخواستی با موفقیت انجام شد."
    INVALID_DATA_FORMAT = "ٔقالب داده‌ی ورودی ناصحیح است."
    MISSING_REQUIRED_FIELDS = "بعضی از فیلد‌های اجباری پر نشده‌اند."
    TRADING_VIEW_NOT_FOUND = "تریدینگ ویوی درخواستی یافت نشد."
    CONNECTED_EXCHANGE_REQUIRED_FOR_TRADING_VIEW_AUTO_TRADE = "برای فعال کردن ترید، ابتدا باید اکسچنج خود را متصل نمایید."
    CONNECTED_TELEGRAM_REQUIRED_FOR_TELEGRAM_NOTIFICATION = ".برای فعال کردن تلگرام، ابتدا باید تلگرام خود را متصل نمایید"
    TELEGRAM_WAS_NOT_NOTIFIED = "در تلگرام ارسال نشد."
    TELEGRAM_NOTIFICATION_FAILED = "خطا! نوتیفیکیشن تلگرام برای ترید ارسال نشد."
    ORDER_WAS_SENT_SUCCESSFULLY = "سفارش با موفقیت ارسال شد."
    ORDER_WAS_FAILED = "دستور ارسال سفارش مشکل دارد، سفارشی ارسال نشد."
    AUTO_TRADING_DISABLED = "ترید خودکار شما غیر فعال است. عملیات شما انجام نشد."
    TRADING_VIEW_WEBHOOK_WORKS = "به رمز ثروت خوش آمدید. تبریک! این صفحه به درستی کار می‌کند."

    # Used in finance/views/watchlist_views.py
    REPEATED_WATCHLIST_NAME = "نام واچ‌لیست تکراری است."
    EMPTY_WATCHLIST_NAME = "نام واچ‌لیست نمی‌تواند خالی باشد."
    SUBSCRIPTION_UPGRADE_NEEDED_FOR_WATCHLIST_CREATION = "برای ساخت واچ‌لیست جدید نیاز به ارتقا اشتراک دارید."
    CANT_DELETE_DEFAULT_WATCHLIST = "حذف واچ لیست پیش فرض امکانپذیر نیست."
    CANNOT_MODIFY_DEFAULT_WATCHLIST = "امکان حذف یا اضافه کردن نماد به واچ‌لیست پیش‌فرض وجود ندارد."
    INVALID_WATCHLIST_ID = "آیدی واچ‌لیست اشتباه است."
    SYMBOL_ALREADY_IN_WATCHLIST = "نماد قبلاً به واچ‌لیست اضافه شده است."
    SYMBOL_ADDED_TO_WATCHLIST = "نماد به واچ‌لیست اضافه شد."
    SYMBOL_REMOVED_FROM_WATCHLIST = "نماد از واچ‌لیست حذف شد."
    INVALID_REQUESTED_ACTION = "عملیات درخواستی نامعتبر است."

    # Used in finance/views/exchange_views.py
    INVALID_ORDER_PAYLOAD = "متغیرهای ورودی سفارش صحیح نمی‌باشد."
    CONNECT_YOUR_EXCHANGE_TO_PLACE_ORDER = "برای ثبت سفارش، ابتدا از تنظیمات اکسچنج خود را متصل کنید."

    # Used in finance/views/market_views.py
    FAILD_TO_GET_SYMBOL = "در دریافت رمزارز درخواستی، مشکلی پیش آمده است."



class TelegramMessage:
    DEPOSIT_REPORT_TEMPLATE = "sold: {init_amount} usdt, final: {final_amount}"

    # Used in finance/views/tradingview_views.py
    ACCOUNT_CONNECTION_GUIDE =  (
        "سلام، برای اتصال تلگرام به حساب خود، پس از ورود به سایت "
        "وارد بخش تنظیمات شوید و کد فعالسازی را ارسال کنید."
    )
    INVALID_ACTIVATION_CODE = "کدفعالسازی اشتباه است."
    ACCOUNT_IS_ALREADY_CONNECTED = "حساب شما به تلگرام متصل است."
    EXPIRED_ACTIVATION_CODE = "کد فعالسازی شما منقضی شده، لطفا کد جدید دریافت کنید."
    ACCOUNT_CONNECTED = "حساب شما به تلگرام متصل شد."

    # Used in xtrader/finance/scan.py
    SUBSCRIPTION_ENDED = "کاربر گرامی اشتراک شما به اتمام رسیده است."
    INSUFFICIENT_WALLET_FUND_FOR_MARKET_SCAN = "کاربر گرامی موجودی کیف پول شما برای پرداخت هزینه اسکن بازار کافی نیست."


class EmailSubject: 
    WELCOME = "خوش‌آمدید!"
