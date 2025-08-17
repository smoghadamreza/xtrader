import json
from typing import cast
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpRequest

from xtrader.data.services.stock_watch_service import StockWatchService
from utils.consts import XtraderResponseKeys


def get_all_symbol_candles_history(_: HttpRequest):
    stock_watch_service = StockWatchService()
    symbols_history = stock_watch_service.get_all_symbol_candles_history() 
    return HttpResponse(json.dumps(symbols_history))


def stock_watch_info(_: HttpRequest, symbol_id: str):
    stock_watch_service = StockWatchService()
    stock_watch_info  = stock_watch_service.get_stock_watch_info(symbol_id=symbol_id)
    return HttpResponse(json.dumps(stock_watch_info))


def symbol_search(_: HttpRequest, query: str):
    stock_watch_service = StockWatchService()
    result  = stock_watch_service.search_symbols(query=query)
    return HttpResponse(
        json.dumps(
            {XtraderResponseKeys.ITEMS: result}, ensure_ascii=False
        ).encode("utf8"),
        content_type="application/json; charset=utf-8",
    )


def get_symbol_candles_history(_: HttpRequest, symbol_id: str, interval: int):
    stock_watch_service = StockWatchService()
    symbol_history_info = stock_watch_service.get_symbol_candles_history(
        symbol_id=symbol_id, interval=interval
    )
    return JsonResponse(json.dumps(symbol_history_info), safe=False)


def get_symbols(_: HttpRequest):
    stock_watch_service = StockWatchService()
    return JsonResponse({
        XtraderResponseKeys.SYMBOLS: 
        stock_watch_service.get_stock_watch_symbols()
    })


def get_all_symbols(_: HttpRequest):
    stock_watch_service = StockWatchService()
    symbols = stock_watch_service.get_all_exchange_symbols()
    data = [{XtraderResponseKeys.TITLE: symbol} for symbol in symbols]
    return JsonResponse({XtraderResponseKeys.SYMBOLS: data})


def get_intervals(request: HttpRequest):
    user = cast(User, request.user)
    stock_watch_service = StockWatchService()
    intervals = stock_watch_service.get_intervals()
    user_time_frame = stock_watch_service.get_user_time_frame(user=user)
    if user_time_frame is None:
        return JsonResponse({XtraderResponseKeys.INTERVALS: intervals})
    return JsonResponse(
        {
            XtraderResponseKeys.INTERVALS: intervals,
            XtraderResponseKeys.USER_TIME_FRAME: user_time_frame
        }
    )
