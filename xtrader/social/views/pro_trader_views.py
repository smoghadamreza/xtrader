from __future__ import annotations
import json
from typing import cast

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from accounts.models import Profile
from accounts.services import TelegramService
from finance.exceptions import NoConnectedExchangeException
from finance.services.exchange.factory import ExchangeServiceFactory
from social.models import ProTrader, Follow
from social.service import ProTraderService
from social.exceptions import NoProTraderFound


@csrf_exempt
@require_GET
def get_pro_traders(request: HttpRequest):
    """Return all pro traders, highlighting followed one if any."""
    follow = Follow.objects.filter(follower=request.user).first()
    protrader_id = follow.pro_trader.pk if follow else 0
    return JsonResponse({"data": ProTrader.get_all(protrader_id)})


@csrf_exempt
@require_POST
def create_pro_trader(request: HttpRequest):
    """Create a new ProTrader for a given user."""
    try:
        data = json.loads(request.body.decode())
        username = data["username"]
        subscription = data["subscription"]

        trader = User.objects.get_by_natural_key(username)
        exchange_service = ExchangeServiceFactory.get_service_for_user(user=trader)

        protrader = ProTrader.objects.create(trader=trader, subscription=subscription)
        exchange_service.get_recent_nav_snapshots()
        return JsonResponse({"e": protrader.pk})
    except Exception as e:
        return JsonResponse({"e": str(e)})


@csrf_exempt
@login_required
def promote_to_pro_trader(request: HttpRequest):
    """Promote the current user to a ProTrader if eligible."""
    if request.method != "POST":
        return JsonResponse({"s": 403, "m": "OK"})

    # Step 1. Check Binance connection
    try:
        ExchangeServiceFactory.get_service_for_user(user=request.user)
    except NoConnectedExchangeException:
        return JsonResponse(
            {"s": 302, "m": "ابتدا حساب خود را به بایننس متصل کنید", "href": "exchange"}
        )

    # Step 2. Check Telegram connection
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or not profile.telegram_id:
        return JsonResponse(
            {"s": 302, "m": "ابتدا حساب خود را به تلگرام متصل کنید", "href": "telegram"}
        )

    # Step 3. Parse request
    data = json.loads(request.body.decode())

    # Step 4. Validation rules
    if ProTrader.objects.filter(brand=data["brand"]).exists():
        return JsonResponse({"s": 200, "m": "این نام نمایشی قبلا استفاده شده است."})

    if Follow.objects.filter(follower=request.user).exists():
        return JsonResponse(
            {"s": 200, "m": "چون شخص دیگری را فالو کرده اید امکان ارتقا حساب وجود ندارد."}
        )

    existing_pro = ProTrader.objects.filter(trader=request.user).first()
    if existing_pro:
        message = (
            "شما قبلا حساب خود را ارتقا داده اید و در انتظار تایید است."
            if existing_pro.status == "PENDING"
            else "شما قبلا حساب خود را ارتقا داده اید."
        )
        return JsonResponse({"s": 200, "m": message})

    # Step 5. Check Binance history
    user = cast(User, request.user)
    pro_service = ProTraderService(pro_user=user)
    if len(pro_service.get_recent_nav_snapshots()) < 28:
        return JsonResponse({"s": 200, "m": "سابقه شما در بایننس کمتر از ۳۰ روز است."})

    # Step 6. Create pending ProTrader
    ProTrader.objects.create(
        trader=request.user,
        brand=data["brand"],
        subscription=float(data["subscription"]),
        status="PENDING",
    )

    TelegramService().send_message(
        message=f'promotion request: {data["brand"]}',
        user_id=settings.ADMIN_TEL_ID,
    )

    return JsonResponse(
        {"s": 200, "m": "حساب شما ارتقا پیدا کرد، پس از تایید نام نمایشی به شبکه اضافه می‌شوید"}
    )
