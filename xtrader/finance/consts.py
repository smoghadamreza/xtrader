class Params:
    TYPE = "type"
    SYMBOL = "symbol"  # Might cause error in OrderAPIClient as it expects "SymbolID"
    ASSET = "asset"

    ORDER_ID = "orderId"
    LIMIT = "limit"

    # Account Service Params
    START_TIME = "startTime"
    END_TIME = "endTime"

    # History Service Params
    FROM_ID = "fromId"

    # Copy-Trade
    # TODO: there is no other reference to this string so I can
    # understand what is it. gonna keep it for backward compatibility.
    ORDER_MARKET_VALUE = "Q"
    ORDER_ACTION = "x"
