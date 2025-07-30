import inspect
import json
import threading
import time
from datetime import datetime
from typing import cast

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from aum.models import Fund
from data.backup import filters_data
from finance import data_handling
from finance import data_handling as dh
from finance import indicator, notification, scan, strategy, volume
from finance.models import TradingView, Watchlist, WatchlistSymbol
from finance.exchange.factory import ExchangeServiceFactory
from finance.exchange.base import BaseExchangeService
from finance.exchange.exception import NoConnectedExchangeException
from finance.exchange.binance.service import binance_market_service
from finance.consts import Params
from finance.models import Exchange
from finance.oms import xtrader_exchange_service

all_functions = dict(inspect.getmembers(data_handling, inspect.isfunction))


def user_exchange_must_be_connected(handler_func):
    def view(request: HttpRequest):
        try:
            exchange_service = ExchangeServiceFactory.get_service_for_user(request.user)
            return handler_func(request, exchange_service)
        except NoConnectedExchangeException as e:
            return JsonResponse({"msg": e.message}, status=403)
    return view


def calculate_indicators(request, interval):
    data = json.loads(request.GET["param"])
    kind = data["kind"].lower()
    function = all_functions["give_result_" + kind]
    result = function(data, interval=interval)
    return JsonResponse(result, safe=False)


@require_POST
@login_required(login_url="accounts:userena_sign_in")
@csrf_exempt
def add_new_watch_list(request):
    watchlist_limit = cast(
        int, strategy.get_pack_limit(request.user).get("watchlist", 0)
    )
    watchlist_count = strategy.get_watchlist_counts(request.user)
    if watchlist_count >= watchlist_limit:
        return JsonResponse(
            {
                "redirect": "/profile-setup/?s=packages",
                "m": "برای ساخت واچ‌لیست جدید نیاز به ارتقا اشتراک دارید",
                "s": 302,
            }
        )
    watchlist_name = request.POST.get("name", "")
    if not watchlist_name:
        return JsonResponse({"m": "name is empty", "s": 403})
    user = request.user
    if not user:
        return JsonResponse({"m": "login required", "s": 403})
    if Watchlist.objects.filter(user=user, name=watchlist_name):
        return JsonResponse({"m": "نام واچ‌لیست تکراری است", "s": 403})
    watchlist = Watchlist(user=user, name=watchlist_name)
    watchlist.save()
    return JsonResponse({"id": watchlist.pk, "s": 200})


@require_GET
@login_required(login_url="accounts:userena_sign_in")
def get_watch_lists(request):
    user = request.user
    if not user:
        return JsonResponse({"m": "login required", "s": 403})
    watchlist_id = request.GET.get("id", "")
    if not watchlist_id:
        watchlists = Watchlist.objects.filter(user=user).order_by("-id")
        result = []
        for watchlist in watchlists:
            result.append(
                {
                    "id": watchlist.pk,
                    "name": watchlist.name,
                }
            )
        result.append(
            {
                "id": 0,
                "name": "پیش فرض",
            }
        )
        return JsonResponse({"watchlists": result, "type": "list", "s": 200})
    else:
        if request.GET.get("action", "add") == "remove":
            if watchlist_id == "0":
                return JsonResponse(
                    {"m": " حذف واچ لیست پیش فرض امکانپذیر نیست.", "s": 403}
                )
            Watchlist.objects.filter(user=user, id=watchlist_id).delete()
            return JsonResponse({"s": 200})
        else:
            return JsonResponse(
                {
                    "symbols": WatchlistSymbol.get_symbols(watchlist_id),
                    "s": 200,
                }
            )

@require_GET
@login_required(login_url="accounts:userena_sign_in")
def update_symbol_to_watch_list(request: HttpRequest) -> JsonResponse:
    user = request.user
    if not user:
        return JsonResponse({"m": "login required", "s": 403})

    watchlist_id = request.GET.get("watchListId", "")
    symbol = request.GET.get("symbol", "BTCUSDT")
    action = request.GET.get("action", "add")
    if watchlist_id == "0":
        return JsonResponse(
            {
                "m": "امکان حذف یا اضافه کردن نماد به"
                " واچ لیست پیش فرض وجود ندارد",
                "s": 403,
            }
        )
    watchlist = Watchlist.objects.filter(user=user, id=watchlist_id).first()
    if not watchlist:
        return JsonResponse({"m": "آیدی واچ لیست اشتباه است", "s": 403})
    if action == "add":
        if WatchlistSymbol.objects.filter(
            watchlist=watchlist, symbol=symbol
        ).first():
            return JsonResponse(
                {"m": "نماد قبلا به واچ لیست اضافه شده است.", "s": 403}
            )
        else:
            WatchlistSymbol(watchlist=watchlist, symbol=symbol).save()
            return JsonResponse({"m": "نماد به واچ لیست اضافه شد.", "s": 200})
    elif action == "remove":
        WatchlistSymbol.objects.filter(
            watchlist=watchlist, symbol=symbol
        ).delete()
        return JsonResponse({"m": "نماد از واچ لیست حذف شد.", "s": 200})

    return JsonResponse({"m": "Invalid action", "s": 400})


@csrf_exempt
def save_strategy(request):
    data = json.loads(request.POST["param"])
    result = strategy.add_strategy_to_db(data, request.user)
    return JsonResponse(result)


def get_strategy_names(request):
    names = strategy.load_strategy_names(request.user)
    return JsonResponse({"strategies": names})


def load_strategy(request):
    strategy_id = int(request.GET["id"])
    filters = strategy.load_strategy_from_db(request.user, strategy_id)
    return JsonResponse(json.dumps(filters), safe=False)


def scan_market(request):
    strategy_id = request.GET.get("strategyId", "")
    if not strategy_id:
        return JsonResponse({}, status=500)
    scan_result = scan.scan_market(request.user, strategy_id)
    return JsonResponse(json.dumps(scan_result), safe=False)


@transaction.atomic
def strategy_notif(request, interval):
    t = threading.Thread(target=scan.screener, args=(interval,))
    t.start()
    if interval == "1d":
        t = threading.Thread(target=Fund.get_daily_snapshots)
        t.start()
    return JsonResponse({"s": "ok"})


@require_GET
def update_indicators(request):
    data = json.loads(request.GET["param"])
    result = data_handling.give_update_indicators(data)
    return JsonResponse(result, safe=False)


@login_required(login_url="accounts:userena_sign_in")
def market_watch(request):
    profile = Profile.objects.get(
        user=User.objects.get_by_natural_key(request.user)
    )
    if not profile.expire or profile.expire >= datetime.today().date():
        return render(
            request, "payment.html", {"subscribes": 0, **get_user(request)}
        )

    return render(request, "marketwatch.html", get_user(request))


@login_required(login_url="accounts:userena_sign_in")
def display(request):
    return render(
        request,
        "back.html",
        {"symbol_id": "BTCUSDT", **get_user(request=request)},
    )


def get_filters(request):
    return HttpResponse(json.dumps(filters_data))


def filter_market(request):
    filters = json.loads(request.GET["filters"])
    import data.dates as d

    last = d.Check().last_market()
    from data.models import MarketWatch

    stocks = MarketWatch.objects.filter(
        stockWatch__LastTradeDate=last
    ).order_by("-stockWatch__TotalTradeValue")
    if len(filters) > 0:
        D = {}
        for f in filters:
            d = json.loads(f)
            D = {**D, **d}
        stocks = stocks.filter(**D)
    paginator = Paginator(stocks, 10)  # Show 25 contacts per page
    page = request.GET.get("page")
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        stocks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        stocks = paginator.page(paginator.num_pages)
    d = {
        "last": paginator.num_pages,
        "former": paginator.num_pages - 1,
        "former2": paginator.num_pages - 2,
    }
    a = render(request, "marketwatchTable.html", {"stocks": stocks, **d})
    return a


@require_GET
def indicators_api(request):
    return JsonResponse(json.dumps(indicator.get_group_api()), safe=False)


@require_GET
def back_test(request):
    data = json.loads(request.GET["param"])
    name = data["name"]
    res = json.loads(data["trades"])
    interval = data["interval"]
    result = dh.give_result_backtest(
        name, res, data["config"], interval=interval
    )
    return JsonResponse(result, safe=False)


def about_us(request):
    return render(request, "aboutus.html", {"username": request.user.username})


@transaction.atomic
def index(request):
    referral_code = request.GET.get("ref", "")
    referred_by = Profile.objects.filter(referral_code=referral_code).first()
    if referral_code and referred_by:
        request.session["ref_id"] = referred_by.pk
    return render(request, "newindex.html")


@login_required(login_url="accounts:userena_sign_in")
def stock_watch(request, symbold_id=None):
    if not symbold_id:
        return redirect("/spot/BTCUSDT")
    return redirect("/spot/" + symbold_id)


@login_required(login_url="accounts:userena_sign_in")
def spot(request, symbol_id: str):
    if not symbol_id:
        return redirect("/spot/BTCUSDT")

    try:
        symbol_info = binance_market_service.get_symbol_info(symbol_id=symbol_id)
    except Exception:
        return render(
            request, "error.html", {"message": "getting symbol info failed."}
        )

    stock_watch_dict = {
        "SymbolId": symbol_id,
        "title": symbol_info.base_asset,
        **get_user(request),
    }
    return render(request, "stockwatch1.html", stock_watch_dict)


def get_user(request):
    username = request.user.username
    user = User.objects.get_by_natural_key(username=username)
    name = user.get_full_name()
    url = (
        "/media/pictures/hadi.jpeg"
        if username == "hadi"
        else "https://www.awicons.com/free-icons/download/"
        "application-icons/dragon-soft-icons-by-artua.com/png/512/User.png"
    )
    return {"name": name, "img_url": url}


def profile_setup(request):
    extra_context = get_user(request)
    return render(request, "setup.html", extra_context)


def ssl(request):
    return HttpResponse(
        "S40flyGXu3pwdfdYzH-MLgUCromgJXv8WMbnAO_LXwE."
        "KJYdMS38SO4zyA2XwO0QVtXlrcWShUZNvEdvbDeDAHc"
    )


@csrf_exempt
def trade(request):
    data = request.POST["order"]
    order = json.loads(data)
    try:
        exchange_service = ExchangeServiceFactory.get_service_from_request(
            request=request
        )
        result = exchange_service.send_order(params=order)
        return JsonResponse(result)
    except ValueError:  # TODO: Use a precise exception
        return JsonResponse(
            {"msg": "ابتدا در تنظیمات اکسچنج خود را متصل کنید"}, status=403
        )

@require_GET
@user_exchange_must_be_connected
def portfolio(_: HttpRequest, exchange_service: BaseExchangeService):
    assets = exchange_service.get_portfolio()
    return JsonResponse({"assets": assets})


@require_GET
@user_exchange_must_be_connected
def get_orders(request: HttpRequest, exchange_service: BaseExchangeService):
    orders = exchange_service.get_orders(
        symbol_id = request.GET[Params.SYMBOL]
    )
    return JsonResponse({"orders": orders})

@user_exchange_must_be_connected
def account_status(_: HttpRequest, exchange_service: BaseExchangeService):
    balance = exchange_service.get_balance()
    return JsonResponse({"buying_power": balance.get("buying_power", None)})

@user_exchange_must_be_connected
def cancel_order(request: HttpRequest, exchange_service: BaseExchangeService):
    result = exchange_service.cancel_order(
        symbol_id=request.GET[Params.SYMBOL],
        order_id=int(request.GET[Params.ORDER_ID])
    )
    if result is None:
        return HttpResponse("e", status=400)
    return HttpResponse("OK", status=200)

def test_volume(request):
    return render(
        request,
        "test_volume.html",
        {"SymbolId": "IRO1IKCO0001", **get_user(request=request)},
    )


def manage_volume(request: HttpRequest):
    data = json.loads(request.GET["param"])
    result = volume.run_test(data)
    return render(request, "volumetest.html", result)


def test_api(request: HttpRequest):
    return render(request, "testAPI.html", {"SymbolId": "IRO1IKCO0001"})


def get_exchanges(request: HttpRequest):
    trader = cast(User, request.user)
    return JsonResponse({"exchanges": Exchange.get_exchanges(trader=trader)})

@require_POST
@csrf_exempt
def save_exchange(request: HttpRequest):
    request_data = cast(dict, request.POST)
    trader = cast(User, request.user)
    return JsonResponse(
        {"status": xtrader_exchange_service.verify_and_create_exchange(
            trader=trader, kwargs=request_data
        )}
    )

@csrf_exempt
def remove_exchange(request: HttpRequest):
    trader = cast(User, request.user)
    result = {
        "status": xtrader_exchange_service.remove_exchange(
            trader=trader, name=request.POST["name"]
        )
    }
    return JsonResponse(result)


@csrf_exempt
@login_required(login_url="accounts:userena_sign_in")
def trading_view(request):
    if request.method == "GET":
        tw, _ = TradingView.objects.get_or_create(
            trader=request.user,
            defaults={
                "webhook": TradingView.create_webhook(),
                "trading": False,
                "notification": False,
            },
        )
        result = {
            "webhook": settings.WEBHOOK_URL_TEMPLATE.format(tw.webhook),
            "trading": tw.trading,
            "notification": tw.notification,
        }
        return JsonResponse(result)
    elif request.method == "POST":
        tw = TradingView.objects.filter(trader=request.user).first()
        if not tw:
            return JsonResponse(
                {"error": "TradingView configuration not found"}, status=404
            )

        try:
            data = json.loads(request.body)
            error = tw.activate(
                trading=data.get("trading", False),
                notification=data.get("notification", False),
            )
            result = {
                "webhook": settings.WEBHOOK_URL_TEMPLATE.format(tw.webhook),
                "trading": tw.trading,
                "notification": tw.notification,
                "msg": error,
            }
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except KeyError:
            return JsonResponse(
                {"error": "Missing required fields"}, status=400
            )

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def trading_view_trade(request, token):
    """
    curl -H 'Content-Type: text/plain; charset=utf-8' -d 'binance spot buy
      btcusdt 0.001 m' -X POST http://127.0.0.1:8000/webhook/3pMoxlHtXT5R
    """
    if request.method == "GET":
        return JsonResponse(
            {
                "Ramzservat": "Welcome to Ramzservat. Congratulations,"
                " this webhook works!",
            }
        )
    if request.method == "POST":
        msg = request.body.decode()
        tw = TradingView.objects.filter(webhook=token).first()
        if not tw:
            return JsonResponse({"msg": "invalid webhook"})
        order_result = ""
        if tw.trading:
            exchange_service = ExchangeServiceFactory.get_service_for_user(
                user=request
            )
            try:
                params = msg.split(" ")
                exchange = params[0].upper()
                if exchange not in ["BINANCE"]:
                    order_result = "نام اکسچنج اشتباه است"
                market = params[1].upper()
                if not order_result and market not in ["SPOT"]:
                    order_result = "نام بازار اشتباه است"
                action = params[2].upper()
                if not order_result and action not in ["BUY", "SELL"]:
                    order_result = "دستور خرید یا فروش است"
                symbol = params[3].upper()
                volume_text = params[4]
                if "%" in volume_text:
                    if "n" in volume_text:
                        quantity = 0
                    else:
                        assets = exchange_service.get_portfolio()
                        ratio = float(volume_text.replace("%", ""))
                        symbol_info = exchange_service.get_symbol_info(
                            symbol_id=symbol
                        )
                        if action == "BUY":
                            value = 12
                            for asset in assets:
                                if asset.symbol == symbol_info.quote_asset:
                                    value = asset.free * (ratio / 100)
                                    break
                            last_price = exchange_service.get_last_price(
                                symbol_id=symbol
                            )  # ticker in legacy. ticker seems wrong.
                            quantity = value / last_price 
                        else:
                            quantity = 0
                            for asset in assets:
                                if asset.symbol == symbol_info.base_asset:
                                    quantity = asset.free * (
                                        ratio / 100
                                    )
                                    break
                else:
                    quantity = float(params[4])
                price = params[5].upper()
                order = {
                    "symbol": symbol,
                    "quantity": quantity,
                    "side": action,
                }
                if price == "M":
                    order["type"] = "MARKET"
                else:
                    order["price"] = float(price)
                    order["type"] = "LIMIT"
                if not order_result:
                    result = exchange_service.send_order(order)
                    if result["error"]:
                        order_result = result["msg"]
                    else:
                        order_result = "سفارش با موفقیت ارسال شد"
            except Exception:
                order_result += "\n"
                order_result += (
                    "دستور ارسال سفارش مشکل دارد، سفارشی ارسال نشد"
                )
        telegram_result = "در تلگرام ارسال نشد"
        if tw.notification:
            profile = Profile.objects.filter(user=tw.trader).first()
            if profile:
                telegram_id = profile.telegram_id
                if order_result:
                    msg += "\n" + str(order_result)
                telegram_result = notification.send_telegram_message(
                    msg, telegram_id
                )
        return JsonResponse(
            {"order": order_result, "telegram": telegram_result}
        )


@csrf_exempt
def telegram_webhook(request):
    """
    curl --tlsv1.2 -v -k -X POST -H "Content-Type: application/json"
      -H "Cache-Control: no-cache"  -d '{
    "update_id":10000,
    "message":{
      "date":1441645532,
      "chat":{
         "last_name":"Test Lastname",
         "id":1111111,
         "first_name":"Test",
         "username":"Test"
      },
      "message_id":1365,
      "from":{
         "last_name":"Test Lastname",
         "id":121366977,
         "first_name":"Test",
         "username":"Test"
      },
      "text":"ON0rtC"
    }
    }' "http://127.0.0.1:8000/telegram-webhook"
    """
    if request.method == "POST":
        data = request.body.decode()
        try:
            data = json.loads(data)
            message = data["message"]
            user_id = message["from"]["id"]
            text = message["text"]
            reply = (
                "سلام، برای اتصال تلگرام به حساب خود، پس از ورود به سایت "
                "وارد بخش تنظیمات شوید و کد فعالسازی را ارسال کنید."
            )
            if not text == "/start":
                profile = Profile.objects.filter(
                    telegram_activation_code=text
                ).first()
                if profile:
                    if (
                        profile.telegram_activation_timestamp
                        and int(time.time())
                        < profile.telegram_activation_timestamp
                    ):
                        profile.telegram_id = str(user_id)
                        profile.save()
                        reply = "حساب شما به تلگرام متصل شد"
                    else:
                        reply = (
                            "کد فعالسازی شما"
                            " منقضی شده، لطفا کد جدید دریافت کنید"
                        )
                else:
                    profile = Profile.objects.filter(
                        telegram_id=str(user_id)
                    ).first()
                    if profile:
                        reply = "حساب شما به تلگرام متصل است"
                    else:
                        reply = "کدفعالسازی اشتباه است"

            notification.send_telegram_message(reply, user_id=user_id)
        except Exception as e:
            print(e)
        return JsonResponse({"msg": "ok"})
    else:
        return JsonResponse({"msg": "are you kidding me?"})


def redi(request):
    return redirect("/")
