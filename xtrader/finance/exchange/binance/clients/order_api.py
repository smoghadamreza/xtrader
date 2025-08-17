
from typing import cast, Dict, Any, Union, List

from .authenticated_api import AuthenticatedAPIClient
from finance.exchange.constants.binance import (
    BinanceRequestKeys, MESSAGE, ERROR, STATUS_CODE,
    INSUFFICIENT_FUNDS_STATUS_CODE, INSUFFICIENT_FUNDS_MESSAGE, 
    INVALID_INPUT_STATUS_CODES, INVALID_INPUT_MESSAGE,
    DEFAULT_ERROR_MESSAGE_TEMPLATE
)
from finance.exchange.data import (
    OrderRequestData, OrderType, SymbolInfo
)


class OrderAPIClient(AuthenticatedAPIClient):
    class Endpoint:
        OPEN_ORDERS = AuthenticatedAPIClient.V3_ENDPOINT + "/openOrders"
        ORDER = AuthenticatedAPIClient.V3_ENDPOINT + "/order"
        OCO = ORDER + "/oco"  # O.C.O: One Cancels the Other

    def send_order(self, params: dict) -> Dict[str, bool|str]:
        """
        Send a new order (MARKET, LIMIT, STOP, OCO, etc.)
        """
        order_data = OrderRequestData.loads(params=params)
        order_data.validate()
        endpoint = self.Endpoint.OCO if order_data.type == OrderType.OCO else self.Endpoint.ORDER
        response = cast(Dict[str, Any], self.post(endpoint=endpoint, params=order_data.to_dict()))
        return self._create_send_order_result(binance_response=response)

    def cancel_order(self, symbol_id: str, order_id: int) -> Union[Dict[str, Any], List[Any]]:
        """
        Cancel a specific order by ID
        """
        params = {
            BinanceRequestKeys.SYMBOL: symbol_id,
            BinanceRequestKeys.ORDER_ID: int(order_id)
        }
        return self.delete(endpoint=self.Endpoint.ORDER, params=params)

    def cancel_all_orders(self, symbol_id: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Cancel all open orders for a symbol
        """
        params = {
            BinanceRequestKeys.SYMBOL: symbol_id.upper()
        }
        return self.delete(endpoint=self.Endpoint.OPEN_ORDERS, params=params)

    def adjust_quantity_to_lot_size(self, symbol_info: SymbolInfo, quantity: float) -> str:  # replaces lot_filter in legacy oms.Binance

        """Apply LOT_SIZE filters to order quantity"""
        
        if not symbol_info.lot_filter:
            return f"{quantity:.8f}"  # Default formatting if no filter found
            
        lot_filter = symbol_info.lot_filter

        clamped_quantity = max(
            lot_filter.min_quantity,
            min(quantity, lot_filter.max_quantity)
        )

        # Round down to the nearest valid step size
        step_count = int(clamped_quantity / lot_filter.step_size)
        adjusted_quantity = step_count * lot_filter.step_size

        # Format the result with appropriate precision
        precision = max(0, symbol_info.base_asset_precision - 1)
        return f"{adjusted_quantity:.{precision}f}"


    @staticmethod
    def _create_send_order_result(binance_response: Dict[str, Any]) -> Dict[str, str|bool]:
        if MESSAGE not in binance_response:
            return {ERROR: False}
        if binance_response.get(STATUS_CODE) == INSUFFICIENT_FUNDS_STATUS_CODE:
            return {
                ERROR: True,
                MESSAGE: INSUFFICIENT_FUNDS_MESSAGE
            }
        if binance_response.get(STATUS_CODE) in INVALID_INPUT_STATUS_CODES:
            return {
                ERROR: True,
                MESSAGE: INVALID_INPUT_MESSAGE
            }
        return {
            ERROR: True,
            MESSAGE: DEFAULT_ERROR_MESSAGE_TEMPLATE.format(
                status_code = binance_response.get(STATUS_CODE)
            )
        }
