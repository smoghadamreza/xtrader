from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from finance.models import Watchlist, WatchlistSymbol
from finance.url_names import FinanceURLS
from finance.services import StrategyService

from utils.consts import (
    XtraderResponseKeys, XtraderRequestKeys, XtraderResponseMessages,
    XtraderRequestValues
)


@require_POST
@login_required
@csrf_exempt
def add_new_watchlist(request: HttpRequest) -> JsonResponse:
    user = request.user
    strategy_service = StrategyService(trader=user)
    watchlist_limit = strategy_service.get_pack_limit().watchlist
    watchlist_count = Watchlist.objects.filter(trader=user).count()
    if watchlist_count >= watchlist_limit:
        return JsonResponse(
            {
                XtraderResponseKeys.REDIRECT: FinanceURLS.SETTINGS_PACKAGES,
                XtraderResponseKeys.M: XtraderResponseMessages.SUBSCRIPTION_UPGRADE_NEEDED_FOR_WATCHLIST_CREATION,
                XtraderResponseKeys.S: 302
            }
        )
    watchlist_name = request.POST.get(XtraderRequestKeys.NAME, "")
    if not watchlist_name:
        return JsonResponse({
            XtraderResponseKeys.M: XtraderResponseMessages.EMPTY_WATCHLIST_NAME,
            XtraderResponseKeys.S: 403
        })
    if Watchlist.objects.filter(user=user, name=watchlist_name).exists():
        return JsonResponse({
            XtraderResponseKeys.M: XtraderResponseMessages.REPEATED_WATCHLIST_NAME,
            XtraderResponseKeys.S: 403
        })
    watchlist = Watchlist.objects.create(user=user, name=watchlist_name)
    return JsonResponse({
        XtraderResponseKeys.ID: watchlist.pk,
        XtraderResponseKeys.S: 200
    })

@require_GET
@login_required
def get_watchlists(request: HttpRequest) -> JsonResponse:
    user = request.user
    watchlist_id = request.GET.get(XtraderRequestKeys.ID, "")
    if not watchlist_id:
        watchlists = Watchlist.objects.filter(user=user).order_by("-id")
        result = [
            {
                XtraderResponseKeys.ID: w.pk,
                XtraderResponseKeys.NAME: w.name
            } for w in watchlists
        ]
        result.append({XtraderResponseKeys.ID: 0, XtraderResponseKeys.NAME: "پیش فرض"})
        return JsonResponse(
            {
                XtraderResponseKeys.WATCHLISTS: result,
                XtraderResponseKeys.TYPE: "list",
                XtraderResponseKeys.S: 200
            }
        )

    action = request.GET.get(XtraderRequestKeys.ACTION, XtraderRequestValues.ADD)
    if action == XtraderRequestValues.REMOVE:
        if watchlist_id == XtraderRequestValues.DEFAULT_WATCHLIST_ID:
            return JsonResponse({
                    XtraderResponseKeys.M: XtraderResponseMessages.CANT_DELETE_DEFAULT_WATCHLIST,
                    XtraderResponseKeys.S: 403
                })
        Watchlist.objects.filter(user=user, id=watchlist_id).delete()
        return JsonResponse({XtraderResponseKeys.S: 200})

    return JsonResponse(
        {
            XtraderResponseKeys.SYMBOLS: WatchlistSymbol.get_symbols(watchlist_id),
            XtraderResponseKeys.S: 200
        }
    )

@login_required
@require_POST
def modify_watchlist_symbol(request: HttpRequest) -> JsonResponse:
    user = request.user
    watchlist_id = request.GET.get(XtraderRequestKeys.WATCHLIST_ID, "")
    symbol = request.GET.get(XtraderRequestKeys.SYMBOL, XtraderRequestValues.BTC_USDT)
    action = request.GET.get(XtraderRequestKeys.ACTION, XtraderRequestValues.ADD)

    if watchlist_id == XtraderRequestValues.DEFAULT_WATCHLIST_ID:
        return JsonResponse({
            XtraderResponseKeys.M: XtraderResponseMessages.CANNOT_MODIFY_DEFAULT_WATCHLIST,
            XtraderResponseKeys.S: 403
        })

    watchlist = Watchlist.objects.filter(user=user, id=watchlist_id).first()
    if not watchlist:
        return JsonResponse({
            XtraderResponseKeys.M: XtraderResponseMessages.INVALID_WATCHLIST_ID,
            XtraderResponseKeys.S: 403
        })

    if action == XtraderRequestValues.ADD:
        if WatchlistSymbol.objects.filter(watchlist=watchlist, symbol=symbol).exists():
            return JsonResponse({
                XtraderResponseKeys.M: XtraderResponseMessages.SYMBOL_ALREADY_IN_WATCHLIST,
                XtraderResponseKeys.S: 403
            })
        WatchlistSymbol.objects.create(watchlist=watchlist, symbol=symbol)
        return JsonResponse({
            XtraderResponseKeys.M: XtraderResponseMessages.SYMBOL_ADDED_TO_WATCHLIST,
            XtraderResponseKeys.S: 200
        })

    if action == XtraderRequestValues.REMOVE:
        WatchlistSymbol.objects.filter(watchlist=watchlist, symbol=symbol).delete()
        return JsonResponse({
            XtraderResponseKeys.M: XtraderResponseMessages.SYMBOL_REMOVED_FROM_WATCHLIST,
            XtraderResponseKeys.S: 200
        })

    return JsonResponse({
        XtraderResponseKeys.M: XtraderResponseMessages.INVALID_REQUESTED_ACTION,
        XtraderResponseKeys.S: 400
    })
