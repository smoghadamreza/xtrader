import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from social.models import Follow


@csrf_exempt
@login_required
def follow_toggle(request):
    """Toggle follow/copy-trade status for a pro trader."""
    if request.method != "POST":
        return JsonResponse({"m": "OK"})

    data = json.loads(request.body.decode())
    result = Follow.copy_trade(
        user=request.user,
        brand=data["protrader_brand"],
        action=data["action"],
    )
    return JsonResponse(result)
