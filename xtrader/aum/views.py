from typing import cast
import json
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from aum.models import Fund, FundInvestor
from aum.service.fund import FundService
from aum.exception import (
    FundInvestorNotFound, FundNotFound, InvalidAction,
    InsufficientDepositInFund, InsufficientUnitsFromInvestor,
    InvestorAlreadyExists, NameIsTooLong
)
from utils.consts import (
    XtraderRequestKeys, XtraderResponseKeys, XtraderRequestValues
)
from .consts import ResponseMessages, ResponseData


@login_required
def management(request):
    return render(request, "fund_management.html")

@csrf_exempt
@require_POST
@login_required
def issue_redeem_unit(request: HttpRequest):
    message = ""
    c = None
    try:
        params = json.loads(request.body.decode())

        fund_manager = cast(User, request.user)
        fund_service = FundService(fund_manager=fund_manager)
        fund_service.issue_redeem_unit(
            investor_id=params[XtraderRequestKeys.INVESTOR_ID],
            action=params[XtraderRequestKeys.ACTION],
            unit_amount=params[XtraderRequestKeys.AMOUNT]
        )
        c = 200
    except FundNotFound:
        message = ResponseMessages.FUND_NOT_FOUND
    except FundInvestorNotFound:
        message = ResponseMessages.FUND_INVESTOR_INVALID_ID
    except InvalidAction:
        message = ResponseMessages.INVALID_ACTION
    except InsufficientDepositInFund:
        message = ResponseMessages.INSUFFICIENT_DEPOSIT_IN_FUND
    except InsufficientUnitsFromInvestor:
        message = ResponseMessages.INSUFFICIENT_UNITS_FROM_INVESTOR

    return JsonResponse(
        {
            XtraderResponseKeys.MESSAGE: message,
            XtraderResponseKeys.C: c
        }
    )

@csrf_exempt
@require_POST
@login_required
def add_investor(request: HttpRequest):
    data = json.loads(request.body.decode())
    try:
        fund = Fund.objects.get(manager=request.user)
        investor = FundInvestor.create_investor(
            fund=fund,
            first_name=data[XtraderRequestKeys.FIRST_NAME],
            last_name=data[XtraderRequestKeys.LAST_NAME],
            national_code=data[XtraderRequestKeys.NATIONAL_CODE]
        )
        return JsonResponse(
        {
            XtraderResponseKeys.MESSAGE: ResponseMessages.CREATED,
            XtraderResponseKeys.ID: investor.pk
        }, status=201
        )
    except Fund.DoesNotExist:
        message = ResponseMessages.FUND_NOT_FOUND
    except NameIsTooLong:
        message = ResponseMessages.NAME_IS_TOO_LONG
    except InvestorAlreadyExists:
        message = ResponseMessages.ALREADY_EXISTS
    return JsonResponse({XtraderResponseKeys.MESSAGE: message}, status=400)

@require_GET
@login_required
def investors(request: HttpRequest):
    try:
        fund_manager = cast(User, request.user)
        service = FundService(fund_manager=fund_manager)
        return JsonResponse({XtraderResponseKeys.DATA: service.get_investors_info()})
    except FundNotFound:
        return JsonResponse({XtraderResponseKeys.MESSAGE: ResponseMessages.FUND_NOT_FOUND})

@require_GET
@login_required
def get_fund(request: HttpRequest):
    fund_manager = cast(User, request.user)
    try:
        fund_service = FundService(fund_manager=fund_manager)
        fund_info = fund_service.get_fund_info()
        return JsonResponse(fund_info)
    except FundNotFound:
        return JsonResponse({})

@require_GET
@login_required
def transactions_history(request: HttpRequest):
    fund_manager = cast(User, request.user)
    fund_service = FundService(fund_manager=fund_manager)
    transactions = fund_service.sync_and_fetch_transactions()
    return JsonResponse({XtraderResponseKeys.DATA: [t.time for t in transactions]})

@require_GET
@login_required
def init_fund_performance(request: HttpRequest):
    pass_value = request.GET.get(XtraderRequestKeys.PASS, "")
    if pass_value != XtraderRequestValues.XTREASURY:
        return JsonResponse({
            XtraderResponseKeys.MESSAGE:
            ResponseMessages.NOT_AUTHORIZED
        }, status=401
        )
    try:
        fund_manager = cast(User, request.user)
        fund_service = FundService(fund_manager=fund_manager)
        created = fund_service.init_fund_performance()
        data = ResponseData.CREATED if created else ResponseData.ALREADY_EXISTS
    except FundNotFound:
        data = []
    return JsonResponse({XtraderResponseKeys.DATA: data})


@require_GET
@login_required
def get_fund_performance(request: HttpRequest):
    try:
        fund_manager = cast(User, request.user)
        fund_service = FundService(fund_manager=fund_manager)
        mode = request.GET.get(
            XtraderRequestKeys.MODE, XtraderRequestValues.ALL
        )
        result = fund_service.get_fund_performance(mode=mode)
    except FundNotFound:
        return JsonResponse([], safe=False)
    return JsonResponse({XtraderResponseKeys.DATA: result}, safe=False)