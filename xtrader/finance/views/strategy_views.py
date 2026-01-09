from __future__ import annotations

import json
import threading

from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
from finance.services.trade_strategy_management import (
    MartingaleStopLossTakeProfitService,
    MartingaleStrategyConfig,
)
from finance.services.exchange.binance.service import binance_market_service
from finance.templates import FinanceTemplates
from finance.exceptions import InvalidIndicatorType, RequiredKeyMissing
from aum.service.fund import FundService
from finance.services import StrategyService
from finance.services.indicators import IndicatorService, indicator_catalog
from finance.services.scan_service import ScanService
from utils.consts import (
    XtraderRequestKeys,
    XtraderResponseKeys,
    XtraderResponseMessages,
    XtraderRequestValues
)


# ---------------------------------------------------------------------
# Indicator Calculation
# ---------------------------------------------------------------------

@require_GET
def calculate_indicators(request: HttpRequest, interval: str) -> JsonResponse:
    """Calculate indicators for a given interval and data payload."""
    try:
        data = json.loads(request.GET[XtraderRequestKeys.PARAM])
        symbol = data[XtraderRequestKeys.SYMBOL_ID]
        service = IndicatorService(symbol=symbol, interval=interval)
        result = service.caculate_indicators(
            request_data=data
        )
        return JsonResponse(result, safe=False)
    except (KeyError, json.JSONDecodeError, RequiredKeyMissing):
        return JsonResponse({
            XtraderResponseKeys.ERROR: XtraderResponseMessages.SOMETHING_WENT_WRONG
        }, status=400)
    except InvalidIndicatorType:
        return JsonResponse({
                XtraderResponseKeys.ERROR:
                XtraderResponseMessages.INVALID_REQUESTED_ACTION
            },status=400)


# ---------------------------------------------------------------------
# Strategy CRUD Operations
# ---------------------------------------------------------------------

@require_POST
@csrf_exempt
def save_strategy(request: HttpRequest) -> JsonResponse:
    """Save a strategy for the current user."""
    try:
        data = json.loads(request.POST[XtraderRequestKeys.PARAM])
        strategy_service = StrategyService(trader=request.user)
        result = strategy_service.add_or_update_strategy(raw_data=data)
        return JsonResponse(result.to_dict())
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({
            XtraderResponseKeys.ERROR: XtraderResponseMessages.SOMETHING_WENT_WRONG
        }, status=400)


@require_GET
def get_strategy_names(request: HttpRequest) -> JsonResponse:
    """Get list of strategy names for the current user."""
    strategy_service = StrategyService(trader=request.user)
    strategies = strategy_service.get_strategies()
    strategy_names = [s.name for s in strategies]
    return JsonResponse({XtraderResponseKeys.STRATEGIES: strategy_names})


@require_GET
def load_strategy(request: HttpRequest) -> JsonResponse:
    """Load strategy details from DB by ID."""
    try:
        strategy_id = int(request.GET[XtraderRequestKeys.ID])
        strategy_service = StrategyService(trader=request.user)
        strategy = strategy_service.get_strategy(strategy_id=strategy_id)
        return JsonResponse(json.dumps(strategy.filters), safe=False)
    except (KeyError, ValueError):
        return JsonResponse({
            XtraderResponseKeys.ERROR: XtraderResponseMessages.INVALID_REQUESTED_ACTION
        }, status=400)


# ---------------------------------------------------------------------
# Market Scanning
# ---------------------------------------------------------------------

@require_GET
def scan_market(request: HttpRequest) -> JsonResponse:
    """Scan the market for a given strategy."""
    strategy_id = request.GET.get(XtraderRequestKeys.STRATEGY_ID)
    if not strategy_id:
        return JsonResponse({}, status=400)

    try:
        # Use ScanService to perform a single-strategy scan.
        # If request contains an explicit interval, use it; otherwise default to '1h'.
        interval = request.GET.get(XtraderRequestKeys.INTERVAL, XtraderRequestValues.Interval.ONE_HOUR)
        scan_service = ScanService(interval=interval)
        # _scan_market expects username + strategy_id; keep former=False like original view did.
        scan_result = scan_service._scan_market(
            username=request.user.username,
            strategy_id=int(strategy_id),
            former=False,
        )
        return JsonResponse(json.dumps(scan_result), safe=False)
    except Exception:
        return JsonResponse({
            XtraderResponseKeys.ERROR: XtraderResponseMessages.SOMETHING_WENT_WRONG
        }, status=400)


@transaction.atomic
@require_GET
def strategy_notif(_: HttpRequest, interval: str) -> JsonResponse:
    """Trigger strategy notifications and optionally snapshot funds."""
    # Start the full screener (all users) using ScanService.run_all_users (threaded)
    threading.Thread(target=ScanService(interval).run_all_users).start()

    # Keep existing daily snapshot behavior
    if interval == XtraderRequestValues.Interval.ONE_DAY:
        threading.Thread(target=FundService.create_today_snapshots).start()

    return JsonResponse({XtraderResponseKeys.S: 200})


# ---------------------------------------------------------------------
# Indicator Catalog API
# ---------------------------------------------------------------------

@require_GET
def indicators_api(_: HttpRequest) -> JsonResponse:
    """Get all available indicator groups API."""
    return JsonResponse(json.dumps(indicator_catalog.get_group_api()), safe=False)


# ---------------------------------------------------------------------
# Backtesting
# ---------------------------------------------------------------------

@require_GET
def back_test(request: HttpRequest) -> JsonResponse:
    """Run a backtest with given configuration using the new IndicatorService."""
    try:
        data = json.loads(request.GET[XtraderRequestKeys.PARAM])
        symbol = data[XtraderRequestKeys.NAME]
        interval = data.get(XtraderRequestKeys.INTERVAL)
        trades = json.loads(data[XtraderRequestKeys.TRADES])
        config = data[XtraderRequestKeys.CONFIG]

        service = IndicatorService(symbol=symbol, interval=interval)
        result = service.give_result_backtest(trades, config)
        return JsonResponse(result, safe=False)
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({
            XtraderResponseKeys.ERROR: XtraderResponseMessages.SOMETHING_WENT_WRONG
        }, status=400)
    
def run_martingale_strategy(request: HttpRequest):
    data = json.loads(request.GET[XtraderRequestKeys.PARAM])
    service = MartingaleStopLossTakeProfitService(
        config=MartingaleStrategyConfig.from_dict(data),
        market_service=binance_market_service,
    )
    result = service.run_strategy()
    return render(request, FinanceTemplates.MARTIN_GALE_STRATEGY_RESULTS, result)
