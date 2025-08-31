from finance.services.exchange.data import OrderRequestData
from utils.consts import XtraderRequestValues

class CopyTradeOrderData:
    UNAVAILABLE_PRICE = -1

    request_data: OrderRequestData
    base_asset: str
    quote_asset: str
    quote_price: float
    order_action: str
    order_market_value: float
    nav_ratio: float = 0.0

class CopyTradeOrderAction:
    NEW = XtraderRequestValues.NEW
    CANCEL = XtraderRequestValues.CANCEL
