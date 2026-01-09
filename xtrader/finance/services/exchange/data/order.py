from dataclasses import dataclass
from typing import Optional, Dict, Any
from finance.services.exchange.constants.binance import BinanceRequestKeys, BinanceRequestValues

class OrderParams:
    SYMBOL = BinanceRequestKeys.SYMBOL  # Might cause error in OrderAPIClient as it expects "SymbolID"
    QUANTITY = BinanceRequestKeys.QUANTITY  #  Might cause error in OrderAPIClient as it expects "Quantity"
    SIDE = BinanceRequestKeys.SIDE  #  Might cause error in OrderAPIClient as it expects "orderSide"
    TYPE = BinanceRequestKeys.TYPE  #  Might cause error in OrderAPIClient as it expects "orderType"
    PRICE = BinanceRequestKeys.PRICE  #  Might cause error in OrderAPIClient as it expects "Price"
    STOP_PRICE = BinanceRequestKeys.STOP_PRICE  #  Might cause error in OrderAPIClient as it expects "stop_price", although this was not anywhere in the codebase. 
    STOP_LIMIT_PRICE = BinanceRequestKeys.STOP_LIMIT_PRICE
    STOP_LIMIT_TIME_IN_FORCE = BinanceRequestKeys.STOP_LIMIT_TIME_IN_FORCE
    TIME_IN_FORCE = BinanceRequestKeys.TIME_IN_FORCE


class OrderType:
    LIMIT = BinanceRequestValues.LIMIT
    LIMIT_MAKER = BinanceRequestValues.LIMIT_MAKER
    STOP_LOSS_LIMIT = BinanceRequestValues.STOP_LOSS_LIMIT
    TAKE_PROFIT_LIMIT = BinanceRequestValues.TAKE_PROFIT_LIMIT
    STOP_LOSS = BinanceRequestValues.STOP_LOSS
    TAKE_PROFIT = BinanceRequestValues.TAKE_PROFIT
    OCO = BinanceRequestValues.OCO
    MARKET = BinanceRequestValues.MARKET


ALL_ORDER_TYPE = set(vars(OrderType).values())
LIMIT_ORDER_TYPES = {
    OrderType.LIMIT,
    OrderType.LIMIT_MAKER,
    OrderType.STOP_LOSS_LIMIT,
    OrderType.TAKE_PROFIT_LIMIT,
}

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
class OrderRequestData:
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
        """Validate presence of required fields for given order type."""
        if not self.type:
            raise ValueError("Order type must be specified for validation.")
        if self.type not in ALL_ORDER_TYPE:
            raise ValueError(f"Invalid order type: {self.type}")

        missing_fields = []
        for field, allowed_types in REQUIRED_FIELDS_TO_ORDER_TYPE.items():
            if self.type in allowed_types:
                if getattr(self, self._field_to_attr(field)) is None:
                    missing_fields.append(field)

        if missing_fields:
            raise ValueError(
                f"Missing required fields for order type {self.type}: {missing_fields}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize only required fields for current order type."""
        if not self.type:
            raise ValueError("Order type must be specified before serialization.")

        result: Dict[str, Any] = {}
        for field, allowed_types in REQUIRED_FIELDS_TO_ORDER_TYPE.items():
            if self.type in allowed_types:
                value = getattr(self, self._field_to_attr(field))
                if value is not None:
                    result[field] = value

        # Binance API doesn’t require TYPE explicitly for OCO
        if self.type == OrderType.OCO and OrderParams.TYPE in result:
            del result[OrderParams.TYPE]

        return result

    @classmethod
    def loads(cls, params: Dict[str, Any]) -> "OrderRequestData":
        """
        Create OrderRequestData from dict-like order_data.
        Example:
            {
                "symbol": "BTCUSDT",
                "quantity": "0.001",
                "side": "BUY",
                "type": "LIMIT",
                "price": "30000",
                "timeInForce": "GTC"
            }
        """
        return cls(
            symbol=params.get(OrderParams.SYMBOL),
            quantity=float(params.get(OrderParams.QUANTITY)),
            side=params.get(OrderParams.SIDE),
            type=params.get(OrderParams.TYPE),
            price=float(params[OrderParams.PRICE]) if OrderParams.PRICE in params else None,
            stop_price=float(params[OrderParams.STOP_PRICE]) if OrderParams.STOP_PRICE in params else None,
            stop_limit_price=float(params[OrderParams.STOP_LIMIT_PRICE]) if OrderParams.STOP_LIMIT_PRICE in params else None,
            time_in_force=params.get(OrderParams.TIME_IN_FORCE, BinanceRequestValues.GTC),
            stop_limit_time_in_force=params.get(OrderParams.STOP_LIMIT_TIME_IN_FORCE, BinanceRequestValues.GTC),
        )
    
    
    @classmethod
    def from_tradingview_request(cls, raw_message: str) -> "OrderRequestData":
        """
        Parse TradingView webhook payload into OrderRequestData.
        Expected format: "BINANCE SPOT BUY BTCUSDT 0.001 M"
        """
        parts = raw_message.strip().split()
        if len(parts) < 6:
            raise ValueError(f"Invalid TradingView payload: {raw_message}")

        exchange, market, action, symbol, volume_text, price_text = parts

        # Side
        side = action.upper()

        # Quantity
        try:
            quantity = float(volume_text.replace("%", "")) if "%" not in volume_text else 0.0
        except ValueError:
            raise ValueError(f"Invalid quantity value: {volume_text}")

        # Order type & price
        if price_text.upper() == "M":
            order_type = OrderType.MARKET
            price = None
        else:
            order_type = OrderType.LIMIT
            try:
                price = float(price_text)
            except ValueError:
                raise ValueError(f"Invalid price value: {price_text}")

        return cls(
            symbol=symbol.upper(),
            quantity=quantity,
            side=side,
            type=order_type,
            price=price,
        )

    def _field_to_attr(self, param_field: str) -> str:
        """Map OrderParams constant to dataclass attribute name."""
        return {
            OrderParams.SYMBOL: "symbol",
            OrderParams.QUANTITY: "quantity",
            OrderParams.SIDE: "side",
            OrderParams.TYPE: "type",
            OrderParams.PRICE: "price",
            OrderParams.STOP_PRICE: "stop_price",
            OrderParams.STOP_LIMIT_PRICE: "stop_limit_price",
            OrderParams.TIME_IN_FORCE: "time_in_force",
            OrderParams.STOP_LIMIT_TIME_IN_FORCE: "stop_limit_time_in_force",
        }[param_field]

