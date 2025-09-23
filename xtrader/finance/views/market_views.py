from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from accounts.models import Profile
from finance.services.exchange.binance.service import binance_market_service
from finance.templates import FinanceTemplates
from data.backup import filters_data
from data.models import MarketWatch
from utils.consts import XtraderRequestKeys, XtraderResponseKeys, XtraderResponseMessages
import utils.dates as dates
from .base_views import get_user_context


# --- Views ---

@login_required
def market_watch(request: HttpRequest) -> HttpResponse:
    """
    Render the market watch page if the user's subscription is active.
    Otherwise, show the payment page.
    """
    profile: Profile = Profile.objects.get(user=request.user)
    today = datetime.today().date()

    if not profile.expire or profile.expire >= today:
        # Subscription inactive or expired → prompt for payment
        context: Dict[str, Any] = {
            XtraderResponseKeys.SUBSCRIBES: 0,
            **get_user_context(request),
        }
        return render(request, FinanceTemplates.PAYMENT, context)

    # Active subscription → show market watch
    return render(request, FinanceTemplates.MARKET_WATCH, get_user_context(request))


def get_filters(_: HttpRequest) -> HttpResponse:
    """
    Return the list of available market filters as a JSON response.
    """
    return HttpResponse(json.dumps(filters_data), content_type="application/json")


@login_required
def display(request: HttpRequest) -> HttpResponse:
    """
    Render the backtesting (robots) page.
    """
    context: Dict[str, Any] = {
        XtraderResponseKeys.SYMBOL_ID: "BTCUSDT",
        **get_user_context(request),
    }
    return render(request, FinanceTemplates.BACK_TEST, context)


def filter_market(request: HttpRequest) -> HttpResponse:
    """
    Filter the MarketWatch entries based on client-provided filters.
    Supports pagination and sorting by trade value.
    """
    filters_raw: list[str] = json.loads(request.GET.get(XtraderRequestKeys.FILTERS, "[]"))
    last_trade_date = dates.Check().last_market()

    stocks = MarketWatch.objects.filter(
        stockWatch__LastTradeDate=last_trade_date
    ).order_by("-stockWatch__total_trade_value")

    # Merge multiple filters into one dictionary
    if filters_raw:
        merged_filters: Dict[str, Any] = {}
        for f in filters_raw:
            merged_filters.update(json.loads(f))
        stocks = stocks.filter(**merged_filters)

    # Pagination
    paginator = Paginator(stocks, 10)
    page = request.GET.get(XtraderRequestKeys.PAGE, "1")

    try:
        stocks_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        stocks_page = paginator.page(1)

    context: Dict[str, Any] = {
        XtraderResponseKeys.STOCKS: stocks_page,
        XtraderResponseKeys.LAST_PAGE: paginator.num_pages,
    }
    return render(request, FinanceTemplates.MARKET_WATCH_TABLE, context)


@login_required
def spot(request: HttpRequest, symbol_id: str | None = None) -> HttpResponse:
    """
    Display spot trading page for the given symbol.
    Redirect to BTCUSDT if no symbol is provided.
    """
    if not symbol_id:
        return redirect(reverse("finance:spot", kwargs={"symbol_id": "BTCUSDT"}))

    try:
        symbol_info = binance_market_service.get_symbol_info(symbol_id)
    except Exception:
        context: Dict[str, Any] = {XtraderResponseKeys.MESSAGE: XtraderResponseMessages.FAILD_TO_GET_SYMBOL}
        return render(request, FinanceTemplates.ERROR, context)

    context: Dict[str, Any] = {
        XtraderResponseKeys.SYMBOL_ID: symbol_id,
        XtraderResponseKeys.TITLE: symbol_info.base_asset,
        **get_user_context(request),
    }
    return render(request, FinanceTemplates.STOCK_WATCH, context)


def stock_watch(_: HttpRequest, symbol_id: str | None = None) -> HttpResponse:
    """
    Redirects to the spot trading page for the given symbol.
    Defaults to BTCUSDT if no symbol is specified.
    """
    if not symbol_id:
        return redirect(reverse("finance:spot", kwargs={"symbol_id": "BTCUSDT"}))
    return redirect(reverse("finance:spot", kwargs={"symbol_id": symbol_id}))
