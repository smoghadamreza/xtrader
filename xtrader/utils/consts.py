class RequestType:
    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"

class Symbol:
    USDT = "USDT"
    BTCUSDT = "BTCUSDT"

class XtraderRequestKeys:
    # used in aum.views
    INVESTOR_ID = "investor_id"
    ACTION = "action"
    AMOUNT = "amount"
    PASS = "pass"
    MODE = "mode"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    NATIONAL_CODE = "nationalCode"

    # used in account.views
    NONCE = "nonce"
    USERNAME = "username"
    

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


class XtraderResponseKeys:
    C = "c"  # TODO: I think this supposed to be status code.
    M = "m"  # TODO: I think this supposed to be message.
    MESSAGE = "msg"
    DATA = "data"
    ID = "id"
    STATUS = "status"

    # used in data.views
    INTERVALS = "intervals"
    USER_TIME_FRAME = "userTimeFrame"
    SYMBOLS = "symbols"
    TITLE = "title"
    ITEMS = "items"

    # used in accounts.views
    FOLLOWING = "following"
    EXCHANGE = "exchange"
    TELEGRAM = "telegram"
    PRO_TRADER = "protrader"
    NEW_DEPOSIT = "newDeposit"
    TELEGRAM_ID = "telegram_id"
    ACTIVATION_CODE = "activation_code"

    # Used in accounts/views/wallet_views.py
    FAILED_COUNT = "failed_count"


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

class TelegramMessage:
    DEPOSIT_REPORT_TEMPLATE = "sold: {init_amount} usdt, final: {final_amount}"

class EmailSubject: 
    WELCOME = "خوش‌آمدید!"
