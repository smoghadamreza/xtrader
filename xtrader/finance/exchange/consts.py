SPOT = "SPOT"
LOT_SIZE = "LOT_SIZE"

MESSAGE = 'msg'
ERROR = "error"
STATUS_CODE = "code"
INSUFFICIENT_FUNDS_STATUS_CODE = -2010
INSUFFICIENT_FUNDS_MESSAGE = "موجودی حساب کافی نیست"
INVALID_INPUT_STATUS_CODES = {-1013, -1111}
INVALID_INPUT_MESSAGE = "تعداد یا قیمت اشتباه وارد شده است"
DEFAULT_ERROR_MESSAGE_TEMPLATE = "لطفا دوباره تلاش کنید کد {status_code}"
BUYING_POWER = "buying_power"



class ResponseKeys:
    # General fields
    SYMBOL = "symbol"
    SYMBOLS = "symbols"
    STATUS = "status"
    PRICE = "price"
    TYPE = "type"
    PERMISSIONS = "permissions"
    ID = "id"
    ASSET = "asset"
    ADDRESS = "address"
    TRANSACTION_ID = "txId"


    # Account-related
    BALANCES = "balances"
    SNAPSHOT_VOLUME_OBJECTS = "snapshotVos"
    UPDATE_TIME = "updateTime"

    # Asset-related
    FREE = "free"
    LOCKED = "locked"

    # Ticker-related (24hr statistics)
    PRICE_CHANGE = "priceChange"
    PRICE_CHANGE_PERCENT = "priceChangePercent"
    WEIGHTED_AVG_PRICE = "weightedAvgPrice"
    PREV_CLOSE_PRICE = "prevClosePrice"
    LAST_PRICE = "lastPrice"
    LAST_QTY = "lastQty"
    BID_PRICE = "bidPrice"
    BID_QUANTITY = "bidQty"
    ASK_PRICE = "askPrice"
    ASK_QUANTITY = "askQty"
    OPEN_PRICE = "openPrice"
    HIGH_PRICE = "highPrice"
    LOW_PRICE = "lowPrice"
    VOLUME = "volume"
    QUOTE_VOLUME = "quoteVolume"
    OPEN_TIME = "openTime"
    CLOSE_TIME = "closeTime"
    FIRST_TRADE_ID = "firstId"
    LAST_TRADE_ID = "lastId"
    TRADE_COUNT = "count"

    # Exchange Info
    FILTER_TYPE = "filterType"
    BASE_ASSET = "baseAsset"
    BASE_ASSET_PRECISION = "baseAssetPrecision"
    QUOTE_ASSET = "quoteAsset"
    QUOTE_PRECISION = "quotePrecision"
    QUOTE_ASSET_PRECISION = "quoteAssetPrecision"
    BASE_COMMISSION_PRECISION = "baseCommissionPrecision"
    QUOTE_COMMISSION_PRECISION = "quoteCommissionPrecision"
    ORDER_TYPES = "orderTypes"
    ICEBERG_ALLOWED = "icebergAllowed"
    OCO_ALLOWED = "ocoAllowed"
    OTO_ALLOWED = "otoAllowed"
    QUOTE_ORDER_QTY_MARKET_ALLOWED = "quoteOrderQtyMarketAllowed"
    ALLOW_TRAILING_STOP = "allowTrailingStop"
    CANCEL_REPLACE_ALLOWED = "cancelReplaceAllowed"
    AMEND_ALLOWED = "amendAllowed"
    IS_SPOT_TRADING_ALLOWED = "isSpotTradingAllowed"
    IS_MARGIN_TRADING_ALLOWED = "isMarginTradingAllowed"
    FILTERS = "filters"
    PERMISSION_SETS = "permissionSets"
    DEFAULT_STP_MODE = "defaultSelfTradePreventionMode"
    ALLOWED_STP_MODES = "allowedSelfTradePreventionModes"
    MIN_QUANTITY = "minQty"
    MAX_QUANTITY = "maxQty"
    STEP_SIZE = "stepSize"


    # Market Depth
    LAST_UPDATE_ID = "lastUpdateId"
    BIDS = "bids"
    ASKS = "asks"

    # Trade Record
    ORDER_ID = "orderId"
    QUANTITY = "qty"
    QUOTE_QUANTITY = "quoteQty"
    COMMISSION = "commission"
    COMMISSION_ASSET = "commissionAsset"
    TIME = "time"
    IS_BUYER = "isBuyer"
    IS_MAKER = "isMaker"
    IS_BEST_MATCH = "isBestMatch"

    # Deposit Record
    DEPOSITS_LIST = "depositList"
    AMOUNT = "amount"
    INSERT_TIME = "insertTime"
    CONFIRM_TIMES = "confirmTimes"
    ADDRESS_TAG = "addressTag"

    # Withdrawal Record
    COIN = "coin"
    TRANSACTION_FEE = "transactionFee"
    NETWORK = "network"
    APPLY_TIME = "applyTime"
    TRANSFER_TYPE = "transferType"
    WITHDRAWAL_LIST = "withdrawList"



