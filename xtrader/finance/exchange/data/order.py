from dataclasses import dataclass
from typing import Optional, Dict, Any

class OrderParams:
    SYMBOL = "symbol"  # Might cause error in OrderAPIClient as it expects "SymbolID"
    QUANTITY = "quantity"  #  Might cause error in OrderAPIClient as it expects "Quantity"
    SIDE = "side"  #  Might cause error in OrderAPIClient as it expects "orderSide"
    TYPE = "type"  #  Might cause error in OrderAPIClient as it expects "orderType"
    PRICE = "price"  #  Might cause error in OrderAPIClient as it expects "Price"
    STOP_PRICE = "stopPrice"  #  Might cause error in OrderAPIClient as it expects "stop_price", although this was not anywhere in the codebase. 
    STOP_LIMIT_PRICE = "stopLimitPrice"
    STOP_LIMIT_TIME_IN_FORCE = "stopLimitTimeInForce"
    TIME_IN_FORCE = "timeInForce"

class OrderSide:
    BUY = "BUY"
    SELL = "SELL"

class OrderType:
    LIMIT = "LIMIT"
    LIMIT_MAKER = "LIMIT_MAKER"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"
    OCO = "OCO"
    MARKET = "MARKET"


ALL_ORDER_TYPE = set(vars(OrderType).values())
LIMIT_ORDER_TYPES = {
    OrderType.LIMIT,
    OrderType.LIMIT_MAKER,
    OrderType.STOP_LOSS_LIMIT,
    OrderType.TAKE_PROFIT_LIMIT,
}


GTC = "GTC"

REQUIRED_FIELDS_TO_ORDER_TYPE = {
    OrderParams.SYMBOL: ALL_ORDER_TYPE,
    OrderParams.QUANTITY: ALL_ORDER_TYPE,
    OrderParams.SIDE: ALL_ORDER_TYPE,
    OrderParams.TYPE: ALL_ORDER_TYPE,
    OrderParams.PRICE: LIMIT_ORDER_TYPES | {OrderType.OCO},
    OrderParams.TIME_IN_FORCE: LIMIT_ORDER_TYPES,
    OrderParams.STOP_PRICE: {
        OrderType.OCO, OrderType.STOP_LOSS, OrderType.STOP_LOSS_LIMIT,
        OrderType.TAKE_PROFIT, OrderType.TAKE_PROFIT_LIMIT
    },
    OrderParams.STOP_LIMIT_PRICE: {OrderType.OCO},
    OrderParams.STOP_LIMIT_TIME_IN_FORCE: {OrderType.OCO}
}

@dataclass
class ExchangeOrderData:
    symbol: str
    quantity: float
    side: str
    type: str

    # Conditional fields
    price: Optional[float] = None
    stop_price: Optional[float] = None
    stop_limit_price: Optional[float] = None
    time_in_force: Optional[str] = None
    stop_limit_time_in_force: Optional[str] = None

    def validate(self) -> None:
        """Validate presence of required fields for given order type"""
        if self.type is None:
            raise ValueError("Order type must be specified for validation.")

        missing_fields = []

        for field, allowed_types in REQUIRED_FIELDS_TO_ORDER_TYPE.items():
            if self.type in allowed_types:
                if getattr(self, self._field_to_attr(field)) is None:
                    missing_fields.append(field)

        if missing_fields:
            raise ValueError(f"Missing required fields for order type {self.type}: {missing_fields}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize only required fields for current order type"""
        if self.type is None:
            raise ValueError("Order type must be specified before serialization.")

        result = {}
        for field, allowed_types in REQUIRED_FIELDS_TO_ORDER_TYPE.items():
            if self.type in allowed_types:
                result[field] = getattr(self, self._field_to_attr(field))

        if self.type == OrderType.OCO:
            del result[OrderParams.TYPE]
        return result

    @classmethod
    def loads(cls, params: Dict[str, Any]) -> "ExchangeOrderData":
        """Create Order from dict"""
        return cls(
            symbol=params[OrderParams.SYMBOL],
            quantity=float(params[OrderParams.QUANTITY]),
            side=params[OrderParams.SIDE],
            type=params[OrderParams.TYPE],
            price=float(params[OrderParams.PRICE]) if OrderParams.PRICE in params else None,
            stop_price=float(params[OrderParams.STOP_PRICE]) if OrderParams.STOP_PRICE in params else None,
            stop_limit_price=float(params[OrderParams.STOP_LIMIT_PRICE]) if OrderParams.STOP_LIMIT_PRICE in params else None,
            time_in_force=params[OrderParams.TIME_IN_FORCE] if OrderParams.TIME_IN_FORCE in params else GTC,
            stop_limit_time_in_force=params[OrderParams.STOP_LIMIT_TIME_IN_FORCE] if OrderParams.STOP_LIMIT_TIME_IN_FORCE in params else GTC,
        )

    def _field_to_attr(self, param_field: str) -> str:
        """Map OrderParams constant to class attribute name"""
        return {
            OrderParams.SYMBOL: "symbol",
            OrderParams.QUANTITY: "quantity",
            OrderParams.SIDE: "side",
            OrderParams.TYPE: "type",
            OrderParams.PRICE: "price",
            OrderParams.STOP_PRICE: "stop_price",
            OrderParams.STOP_LIMIT_PRICE: "stop_limit_price",
            OrderParams.TIME_IN_FORCE: "time_in_force",
            OrderParams.STOP_LIMIT_TIME_IN_FORCE: "stop_limit_time_in_force"
        }[param_field]
    

class CopyTradeOrderData:
    UNAVAILABLE_PRICE = -1

    exchange_order_data: ExchangeOrderData
    base_asset: str
    quote_asset: str
    quote_price: float
    order_action: str
    order_market_value: float
    nav_ratio: float = 0.0

class CopyTradeOrderAction:
    NEW = "NEW"
    CANCEL = "CANCELED"
