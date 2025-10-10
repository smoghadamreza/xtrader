from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from finance.views import get_user_context
from social.models import Follow
from social.service import ProTraderService
from social.exceptions import NoProTraderFound
from social.templates import SocialTemplates


def trader(request):
    return render(request, SocialTemplates.TRADE_PROFILE, get_user_context(request=request))


def get_profile(request, pro_id):
    """Return detailed profile of a pro trader."""
    try:
        service = ProTraderService(pro_id=pro_id)
    except NoProTraderFound:
        return JsonResponse({"s": 302, "href": "/social/copy-trading"})

    pro_trader = service.pro_trader
    history = service.get_records()

    if not request.user:
        status = 0
    else:
        followings = Follow.objects.filter(follower=request.user)
        if followings.filter(pro_trader=pro_trader).first():
            status = 1
        elif followings.exists():
            status = 3
        else:
            status = 2

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
