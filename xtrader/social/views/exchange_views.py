from typing import cast
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from finance.models import Exchange
from finance.services import xtrader_exchange_service


@csrf_exempt
@login_required
def exchange(request: HttpRequest):
    trader = cast(User, request.user)

    if request.method == "GET":
        exchanges = Exchange.get_exchanges(trader=trader)
        return JsonResponse({"exchanges": exchanges})

    if request.method == "POST":
        result = {
            "status": xtrader_exchange_service.verify_and_create_exchange(
                trader=trader, kwargs=request.POST
            )
        }
        return JsonResponse(result)

    return JsonResponse({}, status=400)
