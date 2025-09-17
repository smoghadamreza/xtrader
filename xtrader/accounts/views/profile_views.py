from typing import cast
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import redirect, render

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403
from userena import settings as userena_settings
from userena.decorators import secure_required
from userena.models import UserenaBaseProfile
from userena.utils import get_profile_model
from accounts.forms import (
    EditProfileForm, ChangeEmailForm
)
from utils.consts import RequestType, XtraderRequestKeys, XtraderResponseMessages, XtraderResponseKeys
from accounts.services import AccountStatusService, ProfileService
from accounts.services.exceptions import NoProfileFoundForUser
from accounts.templates import AccountsTemplates


class ProfileViews:
    """Class to group all profile-related views."""

    def account_is_disabled(self, request: HttpRequest, username: str):
        """Checks if the account is disabled, if so, returns the disabled account template."""
        user, profile = ProfileService.get_user_and_profile(username=username)

        if user.is_active:
            raise Http404()

        return render(
            request=request, 
            template_name=AccountsTemplates.USERENA_ACCOUNT_DISABLED,
            context={
                "viewed_user": user,
                "profile": profile,
            }
        )

    @method_decorator(secure_required)
    @method_decorator(csrf_exempt)
    @method_decorator(
        permission_required_or_403(
            "change_profile", (get_profile_model(), "user__username", "username")
        )
    )
    def edit_profile(self, request: HttpRequest, username: str):
        """Edit profile."""
        user, profile = ProfileService.get_user_and_profile(username=username)
        user_initial = {"first_name": user.first_name, "last_name": user.last_name}

        form = EditProfileForm(instance=profile, initial=user_initial)

        if request.method == RequestType.POST:
            form = EditProfileForm(
                request.POST, request.FILES, instance=profile, initial=user_initial
            )

            if form.is_valid():
                form.save()

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(
                        request=request,
                        message=XtraderResponseMessages.PROFILE_IS_UPDATED,
                        fail_silently=True,
                    )

                redirect_to = reverse(
                    "accounts:userena_profile_detail",
                    kwargs={XtraderRequestKeys.USERNAME: username},
                )
                return redirect(redirect_to)

        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_PROFILE_FORM,
            context = {
                "form": form,
                "profile": profile,
            }
        )

    def profile_detail(self, request: HttpRequest, username: str):
        """Detailed view of a user."""
        _, profile = ProfileService.get_user_and_profile(username=username)
        profile = cast(UserenaBaseProfile, profile)

        if not profile.can_view_profile(request.user):
            raise PermissionDenied()

        return render(
            request=request, 
            template_name=userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE,
            context = {
                "profile": profile,
                "hide_email": userena_settings.USERENA_HIDE_EMAIL,
            })

    @method_decorator(login_required)
    def profile_status(self, request: HttpRequest) -> JsonResponse:
        """Get profile status for the user."""
        user = cast(User, request.user)
        status = AccountStatusService.get_profile_status(user=user)
        return JsonResponse(status)


    @method_decorator(login_required)
    @method_decorator(require_GET)
    def telegram_status(self, request: HttpRequest) -> JsonResponse:
        """Check telegram status for the user."""
        user = cast(User, request.user)
        try: 
            profile_service = ProfileService(user=user)
            return JsonResponse({
                XtraderResponseKeys.TELEGRAM_ID: profile_service.has_telegram_id(),
                XtraderResponseKeys.ACTIVATION_CODE: 
                    profile_service.get_telegram_activation_code(),
            })
        except NoProfileFoundForUser:
            return JsonResponse(
                {XtraderResponseKeys.MESSAGE: XtraderResponseMessages.NO_PROFILE_FOR_USER}
            )

    @method_decorator(secure_required)
    @method_decorator(csrf_exempt)
    def email_change(self, request: HttpRequest, username: str):
        """Change email address."""
        request_user = cast(User, request.user)
        user, profile = ProfileService.get_user_and_profile(username=username)
        if request_user.username != user.username:
            raise PermissionDenied()

        form = ChangeEmailForm(user)

        if request.method == RequestType.POST:
            form = ChangeEmailForm(user, request.POST, request.FILES)

            if form.is_valid():
                form.save()

                redirect_to = reverse(
                    "accounts:userena_email_change_complete",
                    kwargs={XtraderRequestKeys.USERNAME: user.username},
                )
                return redirect(redirect_to)

        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_EMAIL_CHANGE_FORM,
            context={
                "form": form,
                "profile": profile
            }
        )
    
    def sign_up_completed(self, request: HttpRequest, username: str):
        context = self._simple_template_render_default_context(username=username)
        context.update({
            "userena_activation_required": (
                userena_settings.USERENA_ACTIVATION_REQUIRED
            ),
            "userena_activation_days": userena_settings.USERENA_ACTIVATION_DAYS,
        })
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_SIGNUP_COMPLETED,
            context=context,
        )

    def email_change_completed(self, request: HttpRequest, username: str):
        context = self._simple_template_render_default_context(username=username)
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_EMAIL_CHANGE_COMPLETED,
            context=context,
        )
    
    def email_change_verification_needed(self, request: HttpRequest, username: str):
        context = self._simple_template_render_default_context(username=username)
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_EMAIL_CHANGE_VERIFICATION,
            context=context,
        )

    def _simple_template_render_default_context(self, username: HttpRequest) -> dict:
        context = dict()
        user, profile = ProfileService.get_user_and_profile(username=username)
        context["viewed_user"] = user
        context["profile"] = profile
        return context



profile_views = ProfileViews()
