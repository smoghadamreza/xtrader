import json
from django.db import transaction
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from finance.services.copy_trade.service import CopyTradeService


@csrf_exempt
@require_POST
@transaction.atomic
def copy_order(request: HttpRequest):
    """Handle copying orders from pro traders."""
    try:
        data = json.loads(request.body.decode())
        service = CopyTradeService(pro_trader_id=int(data.get("id", -1)))
        service.copy_trade(order_params=data["order"])
        return JsonResponse({"m": "ok"})
    except Exception:
        return JsonResponse({"m": "something went wrong"})
