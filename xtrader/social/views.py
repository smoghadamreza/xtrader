import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from finance import notification, oms
from finance.models import Exchange
from finance.views import get_user
from social.models import Follow, ProTrader


@csrf_exempt
def pro_traders(request):
    if request.method == "POST":
        data = request.body.decode()
        try:
            data = json.loads(data)
            username = data["username"]
            brand = data["brand"]
            page_kind = data["page_kind"]
            page_url = data["page_url"]
            subscription = data["subscription"]
            trader = User.objects.get_by_natural_key(username)
            ex_obj, ex = oms.OMSManager.get_exchange(request, trader=trader)
            if not ex_obj:
                return JsonResponse({"o": "noEx"})
            protrader = ProTrader(trader=trader, subscription=subscription)
            protrader.create_pro(
                ex, ex_obj, brand=brand, page_kind=page_kind, page_url=page_url
            )
        except Exception as e:
            return JsonResponse({"e": str(e)})
        return JsonResponse({"e": protrader.pk})
    elif request.method == "GET":
        follow = Follow.objects.filter(follower=request.user).first()
        protrader_id = follow.pro_trader.pk if follow else 0
        return JsonResponse({"data": ProTrader.get_all(protrader_id)})

    return JsonResponse(
            {"e": "Method not allowed."},
            status=405
        )


@csrf_exempt
@login_required(login_url="accounts:userena_signin")
def follow_unfollow(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        protrader_brand = data["protrader_brand"]
        action = data["action"]
        result = Follow.copytrade(
            user=request.user, brand=protrader_brand, action=action
        )
    else:
        result = {"m": "OK"}
    return JsonResponse(result)


@csrf_exempt
def getpublics(request):

    result = []
    for pro in ProTrader.objects.all():
        ex = Exchange.objects.filter(trader=pro.trader).first()
        if ex:
            result.append({"id": pro.pk, "public": ex.public})
    return JsonResponse({"publicKeys": result})


@transaction.atomic
@csrf_exempt
def copy_order(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        pro_id = data.get("id", -1)
        pro = ProTrader.objects.filter(id=pro_id).first()
        if not pro:
            return JsonResponse({"m": "no pro, wrong id"})
        pro.copy_order(data["order"])
        result = {"m": "ok"}
    else:
        result = {"m": "OK"}
    return JsonResponse(result)


@csrf_exempt
@login_required(login_url="accounts:userena_signin")
def promote(request):
    if request.method == "POST":
        ex_obj, ex = oms.OMSManager.get_exchange(request, trader=request.user)
        if not ex_obj:
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
        history = ProTrader.get_history(trader=request.user)
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
        notification.send_telegram_message(
            f'promotion request: {data["brand"]}',
            user_id=settings.ADMIN_TEL_ID,
        )
    else:
        result = {"s": 403, "m": "OK"}
    return JsonResponse(result)


def trader(request):
    return render(request, "traderProfile.html", get_user(request=request))


def get_profile(request, pro_id):
    try:
        pro = ProTrader.objects.filter(id=pro_id).first()
        if not pro:
            return JsonResponse({"s": 302, "href": "/social/copytrading"})
    except Exception:
        return JsonResponse({"s": 302, "href": "/social/copytrading"})
    history = ProTrader.get_records(trader=pro.trader)
    if not request.user:
        status = 0  # unknown
    else:
        followings = Follow.objects.filter(follower=request.user)
        if followings:
            if followings.filter(proTrader=pro).first():
                status = 1  # following
            else:
                status = 3  # following someone else
        else:
            status = 2  # not following
    return JsonResponse(
        {
            "s": 200,
            "proTraderBrand": pro.brand,
            "subsFee": pro.subscription,
            "history": history,
            "status": status,
        }
    )


@login_required(login_url="accounts:userena_signin")
def copytrading(request):
    return render(request, "copytrading.html", get_user(request=request))


def league(request):
    return render(request, "leagueLanding.html", get_user(request=request))


@login_required(login_url="accounts:userena_signin")
@csrf_exempt
def exchange(request):
    if request.method == "GET":
        exs = oms.OMSManager.get_exchanges(request)
        return JsonResponse({"exchanges": exs})
    elif request.method == "POST":
        public = request.POST.get("public", None)
        private = request.POST.get("secret", None)
        name = request.POST.get("name", None)
        _exchange = request.POST.get("exchange", None)
        if (
            public is None
            or private is None
            or name is None
            or _exchange is None
        ):
            return JsonResponse({"status": False})
        result = {
            "status": oms.OMSManager.verify_and_create_exchange(
                trader=request.user,
                name=name,
                public=public,
                private=private,
                exchange=_exchange.upper(),
            )
        }
        return JsonResponse(result)
    else:
        return JsonResponse({}, status=400)
