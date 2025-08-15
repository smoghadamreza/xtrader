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
    MESSAGE = "msg"
    DATA = "data"
    ID = "id"

    # used in data.views
    INTERVALS = "intervals"
    USER_TIME_FRAME = "userTimeFrame"
    SYMBOLS = "symbols"
    TITLE = "title"
    ITEMS = "items"

    # used in account.views
    FOLLOWING = "following"
    EXCHANGE = "exchange"
    TELEGRAM = "telegram"
    PRO_TRADER = "protrader"