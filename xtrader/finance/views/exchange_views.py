from __future__ import annotations

import json
from typing import Any, Callable, Dict, TypeVar, cast

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from finance.models import Exchange
from finance.services.exchange.constants.binance import BinanceRequestKeys
from finance.services.exchange.factory import ExchangeServiceFactory
from finance.services import xtrader_exchange_service
from finance.services.exchange.base import BaseExchangeService
from finance.exceptions import NoConnectedExchangeException
from utils.consts import XtraderResponseKeys, XtraderRequestKeys, XtraderResponseMessages


F = TypeVar("F", bound=Callable[..., HttpResponse | JsonResponse])


def user_exchange_must_be_connected(handler_func: F) -> F:
    """
    Decorator ensuring that the requesting user has a connected exchange.
    If not, returns a 403 JsonResponse with an appropriate message.
    """

    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | JsonResponse:
        try:
            exchange_service: BaseExchangeService = ExchangeServiceFactory.get_service_for_user(request.user)
            return handler_func(request, exchange_service, *args, **kwargs)
        except NoConnectedExchangeException as e:
            return JsonResponse({XtraderResponseKeys.MESSAGE: e.message}, status=403)

    return cast(F, wrapper)


@csrf_exempt
def trade(request: HttpRequest) -> JsonResponse:
    """
    Execute a trade order through the connected exchange.
    Expects 'order' in POST data as a JSON string.
    """
    try:
        data: Dict[str, Any] = json.loads(request.POST[XtraderRequestKeys.ORDER])
        exchange_service: BaseExchangeService = ExchangeServiceFactory.get_service_from_request(request)
        result: Dict[str, Any] = exchange_service.send_order(params=data)
        return JsonResponse(result)
    except (KeyError, json.JSONDecodeError):
        return JsonResponse(
            {XtraderResponseKeys.MESSAGE: XtraderResponseMessages.INVALID_ORDER_PAYLOAD}, status=400
        )
    except ValueError:
        return JsonResponse(
            {XtraderResponseKeys.MESSAGE: XtraderResponseMessages.CONNECT_YOUR_EXCHANGE_TO_PLACE_ORDER},
            status=403,
        )


@require_GET
@user_exchange_must_be_connected
def portfolio(_: HttpRequest, exchange_service: BaseExchangeService) -> JsonResponse:
    """
    Retrieve user's portfolio (list of assets) from connected exchange.
    """
    assets: list[Dict[str, Any]] = exchange_service.get_portfolio()
    return JsonResponse({XtraderResponseKeys.ASSETS: assets})


@require_GET
@user_exchange_must_be_connected
def get_orders(request: HttpRequest, exchange_service: BaseExchangeService) -> JsonResponse:
    """
    Get all active orders for a given symbol from connected exchange.
    """
    symbol: str = request.GET[BinanceRequestKeys.SYMBOL]
    orders: list[Dict[str, Any]] = exchange_service.get_orders(symbol_id=symbol)
    return JsonResponse({XtraderResponseKeys.ORDERS: orders})


@require_GET
@user_exchange_must_be_connected
def cancel_order(request: HttpRequest, exchange_service: BaseExchangeService) -> HttpResponse:
    """
    Cancel an order for a given symbol and order ID.
    """
    symbol: str = request.GET[BinanceRequestKeys.SYMBOL]
    order_id: int = int(request.GET[BinanceRequestKeys.ORDER_ID])
    result: bool = exchange_service.cancel_order(symbol_id=symbol, order_id=order_id)

    status_code: int = 200 if result else 400
    response_text: str = "OK" if result else "e"
    return HttpResponse(response_text, status=status_code)


@require_GET
def get_exchanges(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all exchanges associated with the current trader.
    """
    trader: User = cast(User, request.user)
    exchanges: list[Dict[str, Any]] = Exchange.get_exchanges(trader=trader)
    return JsonResponse({XtraderResponseKeys.EXCHANGES: exchanges})


@require_POST
@csrf_exempt
def save_exchange(request: HttpRequest) -> JsonResponse:
    """
    Verify and save a new exchange configuration for the user.
    """
    trader: User = cast(User, request.user)
    result: bool = xtrader_exchange_service.verify_and_create_exchange(trader, request.POST)
    return JsonResponse({XtraderResponseKeys.STATUS: result})


@require_POST
@csrf_exempt
def remove_exchange(request: HttpRequest) -> JsonResponse:
    """
    Remove an existing exchange for the user.
    """
    trader: User = cast(User, request.user)
    exchange_name: str = request.POST.get(XtraderRequestKeys.NAME, "")
    result: bool = xtrader_exchange_service.remove_exchange(trader, exchange_name)
    return JsonResponse({XtraderResponseKeys.STATUS: result})
