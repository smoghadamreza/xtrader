from __future__ import annotations

from typing import Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import Profile
from finance.templates import FinanceTemplates
from utils.consts import XtraderRequestKeys, XtraderResponseKeys


# --- Constants ---

DEFAULT_AVATAR_URL: str = (
    "https://www.awicons.com/free-icons/download/application-icons/"
    "dragon-soft-icons-by-artua.com/png/512/User.png"
)

CUSTOM_AVATARS: Dict[str, str] = {
    "hadi": "/media/pictures/hadi.jpeg",
}


# --- Utility Functions ---

def get_user_context(request: HttpRequest) -> Dict[str, str]:
    """
    Return a standardized context dictionary for rendering user profile-related pages.
    """
    user: User = request.user
    img_url: str = CUSTOM_AVATARS.get(user.username, DEFAULT_AVATAR_URL)

    return {
        XtraderResponseKeys.NAME: user.get_full_name(),
        XtraderResponseKeys.IMAGE_URL: img_url,
    }

# --- Views ---

def index(request: HttpRequest) -> HttpResponse:
    """
    Landing page view.
    Handles referral codes and stores referring user's ID in session.
    """
    referral_code: str = request.GET.get(XtraderRequestKeys.REFERRAL_CODE, "")

    if referral_code:
        referred_by: Profile | None = Profile.objects.filter(
            referral_code=referral_code
        ).first()
        if referred_by:
            request.session["ref_id"] = referred_by.pk

    return render(request, FinanceTemplates.INDEX)


def about_us(request: HttpRequest) -> HttpResponse:
    """
    Render the 'About Us' page with the current user's username.
    """
    context: Dict[str, str] = {XtraderResponseKeys.NAME: request.user.username}
    return render(request, FinanceTemplates.ABOUT_US, context)


def ssl(ـ: HttpRequest) -> HttpResponse:
    """
    SSL verification endpoint for domain ownership checks.
    Returns a fixed verification string.
    """
    verification_token: str = (
        "S40flyGXu3pwdfdYzH-MLgUCromgJXv8WMbnAO_LXwE."
        "KJYdMS38SO4zyA2XwO0QVtXlrcWShUZNvEdvbDeDAHc"
    )
    return HttpResponse(verification_token)


def profile_settings(request: HttpRequest) -> HttpResponse:
    """
    Render user profile settings page with user context.
    """
    context: Dict[str, str] = get_user_context(request)
    return render(request, FinanceTemplates.SETTINGS, context)
