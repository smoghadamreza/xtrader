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
from aum.service import FundService
from aum.exception import (
    FundInvestorNotFound, FundNotFound, InvalidAction,
    InsufficientDepositInFund, InsufficientUnitsFromInvestor
)
from utils.consts import XtraderRequestKeys, XtraderResponseKeys
from .consts import ResponseMessages


@login_required(login_url="accounts:userena_sign_in")
def management(request):
    return render(request, "fundManagement.html")


@csrf_exempt
@require_POST
@login_required(login_url="accounts:userena_sign_in")
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
@login_required(login_url="accounts:userena_sign_in")
def add_investor(request: HttpRequest):
    params = json.loads(request.body.decode())
    national_code = params["nationalCode"]
    fund = Fund.objects.filter(manager=request.user).first()
    if FundInvestor.objects.filter(
        nationalCode=national_code, fund=fund
    ).first():
        result = {"msg": "investor already exists!"}
    elif len(params["first_name"]) > 20 or len(params["last_name"]) > 20:
        result = {
            "msg": "firstName or lastName must be less than 20 characters!"
        }
    else:
        params["fund"] = fund
        investor = FundInvestor(**params)
        investor.save()
        result = {"c": 200, "msg": "investor already exists!"}
    return JsonResponse(result)


@require_GET
@login_required(login_url="accounts:userena_sign_in")
def investors(request: HttpRequest):
    fund = Fund.objects.filter(manager=request.user).first()
    investors = FundInvestor.objects.filter(fund=fund)
    result = []
    for investor in investors:
        result.append(
            {
                "id": investor.pk,
                "name": "{} {}".format(
                    investor.first_name, investor.last_name
                ),
                "units": investor.units,
                "national_code": investor.nationalCode,
            }
        )
    return JsonResponse({"data": result})

@require_GET
@login_required(login_url="accounts:userena_sign_in")
def get_fund(request: HttpRequest):
    fund_manager = cast(User, request.user)
    try:
        fund_service = FundService(fund_manager=fund_manager)
        fund_info = fund_service.get_fund_info()
        return JsonResponse(fund_info)
    except FundNotFound:
        return JsonResponse({})

@require_GET
@login_required(login_url="accounts:userena_sign_in")
def transactions_history(request: HttpRequest):
    fund_manager = cast(User, request.user)
    fund_service = FundService(fund_manager=fund_manager)
    transactions = fund_service.sync_and_fetch_transactions()
    return JsonResponse({"data": [t.time for t in transactions]})

@require_GET
@login_required(login_url="accounts:userena_sign_in")
def init_fund_performance(request: HttpRequest):
    if not request.GET.get("pass", "") == "XTreasury":
        return JsonResponse({"msg": "not authorize"}, status=401)
    fund = Fund.objects.filter(manager=request.user).first()
    result = []
    if fund:
        result = fund.init_fund_performance()
    return JsonResponse({"data": result})


@require_GET
@login_required(login_url="accounts:userena_sign_in")
def get_fund_performance(request: HttpRequest):
    fund = Fund.objects.filter(manager=request.user).first()
    result = []
    if fund:
        mode = request.GET.get("mode", "all")
        result = fund.get_fund_performance(mode=mode)
    return JsonResponse(result, safe=False)
