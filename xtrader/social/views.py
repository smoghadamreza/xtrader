from typing import cast
import json

from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from accounts.services import TelegramService
from finance.models import Exchange
from finance.views import get_user_context
from social.models import Follow, ProTrader
from finance.exceptions import NoConnectedExchangeException
from finance.services.exchange.factory import ExchangeServiceFactory
from finance.services import xtrader_exchange_service
from social.service import ProTraderService
from social.exceptions import NoProTraderFound
from finance.services.copy_trade.service import CopyTradeService
from social.templates import SocialTemplates



@csrf_exempt
def pro_traders(request):
    if request.method == "POST":
        data = request.body.decode()
        try:
            data = json.loads(data)
            username = data["username"]
            subscription = data["subscription"]
            trader = User.objects.get_by_natural_key(username)
            exchange_service = ExchangeServiceFactory.get_service_for_user(user=trader)

            protrader = ProTrader.objects.create(trader=trader, subscription=subscription)
            exchange_service.get_recent_nav_snapshots()
        except Exception as e:
            return JsonResponse({"e": str(e)})
        return JsonResponse({"e": protrader.pk})
    elif request.method == "GET":
        follow = Follow.objects.filter(follower=request.user).first()
        protrader_id = follow.pro_trader.pk if follow else 0
        return JsonResponse({"data": ProTrader.get_all(protrader_id)})

    return JsonResponse({"e": "Method not allowed."}, status=405)


@csrf_exempt
@login_required
def follow_toggle(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        protrader_brand = data["protrader_brand"]
        action = data["action"]
        result = Follow.copy_trade(
            user=request.user, brand=protrader_brand, action=action
        )
    else:
        result = {"m": "OK"}
    return JsonResponse(result)


@require_GET
@csrf_exempt
def get_publics(_: HttpRequest):

    result = []
    for pro in ProTrader.objects.all():
        ex = Exchange.objects.filter(trader=pro.trader).first()
        if ex:
            result.append({"id": pro.pk, "public": ex.public_key})
    return JsonResponse({"publicKeys": result})

@require_POST
@transaction.atomic
@csrf_exempt
def copy_order(request: HttpRequest):
    try:
        data = json.loads(request.body.decode())
        copy_trade_service = CopyTradeService(
            pro_trader_id=int(data.get("id", -1))
        )
        copy_trade_service.copy_trade(order_params=data["order"])
        return  JsonResponse({"m": "ok"})
    except Exception:
        pass
    return JsonResponse({"m": "something went wrong"})


@csrf_exempt
@login_required
def promote(request: HttpRequest):
    if request.method == "POST":
        try:
            exchange_service = ExchangeServiceFactory.get_service_for_user(user=request.user)
        except NoConnectedExchangeException:
            return JsonResponse(
                {
                    "s": 302,
                    "m": "ابتدا حساب خود را به بایننس متصل کنید",
                    "href": "exchange",
                }
            )
        pro = Profile.objects.filter(user=request.user).first()
        if not pro or not pro.telegram_id:
            return JsonResponse(
                {
                    "s": 302,
                    "m": "ابتدا حساب خود را به تلگرام متصل کنید",
                    "href": "telegram",
                }
            )
        data = json.loads(request.body.decode())
        if ProTrader.objects.filter(brand=data["brand"]).first():
            return JsonResponse(
                {"s": 200, "m": "این نام نمایشی قبلا استفاده شده است."}
            )
        if Follow.objects.filter(follower=request.user).first():
            return JsonResponse(
                {
                    "s": 200,
                    "m": "چون شخص دیگری را فالو کرده اید امکان ارتقا حساب وجود ندارد.",
                }
            )
        pro = ProTrader.objects.filter(trader=request.user).first()
        if pro:
            if pro.status == "PENDING":
                return JsonResponse(
                    {
                        "s": 200,
                        "m": "شما قبلا حساب خود را ارتقا داده اید و در انتظار تایید است.",
                    }
                )
            else:
                return JsonResponse(
                    {"s": 200, "m": "شما قبلا حساب خود را ارتقا داده اید."}
                )
        user = cast(User, request.user)
        pro_trader_service = ProTraderService(pro_user=user)
        history = pro_trader_service.get_recent_nav_snapshots()
        if len(history) < 28:
            return JsonResponse(
                {"s": 200, "m": "سابقه شما در بایننس کمتر از ۳۰ روز است."}
            )
        pro = ProTrader(
            trader=request.user,
            brand=data["brand"],
            subscription=float(data["subscription"]),
            status="PENDING",
        )
        pro.save()
        result = {
            "s": 200,
            "m": "حساب شما ارتقا پیدا کرد، پس از تایید نام نمایشی به شبکه اضافه می‌شوید",
        }
        TelegramService().send_message(
            message=f'promotion request: {data["brand"]}',
            user_id=settings.ADMIN_TEL_ID,
        )
    else:
        result = {"s": 403, "m": "OK"}
    return JsonResponse(result)


def trader(request):
    return render(request, SocialTemplates.TRADE_PROFILE, get_user_context(request=request))


def get_profile(request, pro_id):

    try:
        pro_trader_service = ProTraderService(pro_id=pro_id)
    except NoProTraderFound:
        return JsonResponse({"s": 302, "href": "/social/copy-trading"})
    history = pro_trader_service.get_records()
    pro_trader = pro_trader_service.pro_trader
    if not request.user:
        status = 0  # unknown
    else:
        followings = Follow.objects.filter(follower=request.user)
        if followings:
            if followings.filter(pro_trader=pro_trader).first():
                status = 1  # following
            else:
                status = 3  # following someone else
        else:
            status = 2  # not following
    return JsonResponse(
        {
            "s": 200,
            "proTraderBrand": pro_trader.brand,
            "subsFee": pro_trader.subscription,
            "history": history,
            "status": status,
        }
    )


@login_required
def copy_trading(request):
    return render(request, SocialTemplates.COPY_TRADING, get_user_context(request=request))


def league(request):
    return render(request, SocialTemplates.LEAGUE_LANDING, get_user_context(request=request))


@login_required
@csrf_exempt
def exchange(request: HttpRequest):
    trader = cast(User, request.user)
    if request.method == "GET":
        return JsonResponse({"exchanges": Exchange.get_exchanges(trader=trader)})
    elif request.method == "POST":
        request_data = cast(dict, request.POST)
        result = {
            "status": xtrader_exchange_service.verify_and_create_exchange(
                trader=trader, kwargs=request_data)
        }
        return JsonResponse(result)
    else:
        return JsonResponse({}, status=400)
