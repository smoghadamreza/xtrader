from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from finance.models import Exchange
from social.models import ProTrader


@csrf_exempt
@require_GET
def get_publics(_: HttpRequest):
    """Return public keys of all pro traders."""
    result = []
    for pro in ProTrader.objects.all():
        ex = Exchange.objects.filter(trader=pro.trader).first()
        if ex:
            result.append({"id": pro.pk, "public": ex.public_key})
    return JsonResponse({"publicKeys": result})
