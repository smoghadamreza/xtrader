from collections import OrderedDict
from typing import cast

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponseRedirect, JsonResponse, HttpRequest
)
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render

from userena.decorators import secure_required
from userena import settings as userena_settings
from userena import signals as userena_signals
from userena.models import (
    UserenaManager,
    UserenaSignup,
)
from userena.utils import signin_redirect

from accounts.forms import (
    AuthenticationForm,
    SignupFormExtra,
)
from accounts.services import UserActivationService
from utils.consts import (
    RequestType, XtraderRequestKeys,
    XtraderResponseMessages, XtraderResponseKeys
)
from accounts.templates import AccountsTemplates
from accounts.url_names import AccountsURLS
from accounts.services import ProfileService

class AuthenticationViews:
    """Class to group all authentication-related views."""
    
    @method_decorator(secure_required)
    @method_decorator(csrf_exempt)
    def sign_up(self, request: HttpRequest):
        if userena_settings.USERENA_DISABLE_SIGNUP:
            raise PermissionDenied()

        form = SignupFormExtra()
        if request.method == RequestType.POST:
            form = SignupFormExtra(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                userena_signals.signup_complete.send(sender=None, user=user)
                
                redirect_to = reverse(
                    AccountsURLS.SIGNUP_COMPLETED,
                    kwargs={XtraderRequestKeys.USERNAME: user.username},
                )

                if request.user.is_authenticated:
                    logout(request)

                if (userena_settings.USERENA_SIGNIN_AFTER_SIGNUP and 
                    not userena_settings.USERENA_ACTIVATION_REQUIRED):
                    user = authenticate(
                        identification=user.email, check_password=False
                    )
                    login(request, user)

                return redirect(redirect_to)

        form_order = [
            "first_name", "last_name", "username", "cellPhone", "email",
            "password1", "password2",
        ]
        new_form = OrderedDict()
        for k in form_order:
            new_form[k] = form[k]
        form.fields = new_form

        context = {"form": form}
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_SIGNUP_FORM,
            context=context
        )

    @method_decorator(secure_required)
    def sign_in(self, request: HttpRequest):
        """Signin using email or username with password."""
        form = AuthenticationForm()

        if request.method == RequestType.POST:
            form = AuthenticationForm(request.POST, request.FILES)
            if form.is_valid():
                identification, password, remember_me = (
                    form.cleaned_data["identification"],
                    form.cleaned_data["password"],
                    form.cleaned_data["remember_me"],
                )
                user = authenticate(identification=identification, password=password)
                if user is None:
                    raise ValueError("user can not be None")

                if user.is_active:
                    login(request, user)

                    if remember_me:
                        request.session.set_expiry(
                            userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400
                        )
                    else:
                        request.session.set_expiry(0)

                    if userena_settings.USERENA_USE_MESSAGES:
                        messages.success(
                            request,
                            XtraderResponseMessages.SIGNIN_SUCCESS,
                            fail_silently=True,
                        )

                    userena_signals.account_signin.send(sender=None, user=user)

                    redirect_to = signin_redirect(
                        request.GET.get(
                            REDIRECT_FIELD_NAME,
                            request.POST.get(REDIRECT_FIELD_NAME),
                        ),
                        user,
                    )
                    return HttpResponseRedirect(redirect_to)

                else:  # user is inactive
                    signup: UserenaSignup = getattr(user, "userena_signup")
                    if signup.activation_completed:
                        return redirect(
                            reverse(
                                AccountsURLS.ACCOUNT_DISABLED,
                                kwargs={XtraderRequestKeys.USERNAME: user.username},
                            )
                        )
                    else:
                        return redirect(
                            reverse(
                                AccountsURLS.ACCOUNT_ACTIVATION_PENDING,
                                kwargs={XtraderRequestKeys.USERNAME: user.username},
                            )
                        )

        context = {
            "form": form,
            "next": request.GET.get(
                REDIRECT_FIELD_NAME, request.POST.get(REDIRECT_FIELD_NAME)
            ),
        }
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_SIGNIN_FORM,
            context=context,
        )

    @method_decorator(secure_required)
    def sign_out(self, request: HttpRequest):
        if request.user.is_authenticated and userena_settings.USERENA_USE_MESSAGES:
            messages.success(
                request, XtraderResponseMessages.SIGNOUT_SUCCESS, fail_silently=True
            )

        userena_signals.account_signout.send(sender=None, user=request.user)
        logout(request)
        return JsonResponse({})

    @method_decorator(secure_required)
    def activate(self, request: HttpRequest, activation_key: str):
        """Activate a user with an activation key."""
        user, error_message = UserActivationService.activate_user(
            activation_key=activation_key,
            request=request,
        )

        if user:
            return JsonResponse({})
        elif error_message == "invalid link":
            return JsonResponse(
                {XtraderResponseKeys.MESSAGE: XtraderResponseMessages.ACTIVATION_LINK_INVALID},
                status=400,
            )
        elif error_message == "link expired, you should retry":
            return JsonResponse(
                {XtraderResponseKeys.MESSAGE: XtraderResponseMessages.ACTIVATION_LINK_EXPIRED_RETRY}
            )
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_ACTIVATION_FAILED,
            context={},
        )


    def activate_pending(self, request: HttpRequest, username: str):
        """Checks if the account is not active, if so, returns the activation pending template."""
        user = get_object_or_404(
            get_user_model(), username__iexact=username, is_active=False
        )

        signup: UserenaSignup = getattr(user, "userena_sign_up")
        if signup.activation_completed:
            return redirect(
                reverse(
                    AccountsURLS.ACCOUNT_DISABLED,
                    kwargs={XtraderRequestKeys.USERNAME: user.username},
                )
            )

        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_ACTIVATION_PENDING,
            context={},
        )

    @method_decorator(secure_required)
    def activate_retry(self, _: HttpRequest, activation_key: str) -> JsonResponse:
        """Reissue a new activation_key for the user with the expired activation_key."""
        if not userena_settings.USERENA_ACTIVATION_RETRY:
            return redirect(reverse("userena_activate", args=(activation_key,)))
        
        new_key = UserActivationService.reissue_activation(
            activation_key=activation_key)
        if new_key:
            return JsonResponse({})
        return JsonResponse(
            {
                XtraderResponseKeys.MESSAGE:
                XtraderResponseMessages.ACTIVATION_LINK_NOT_EXPIRED
            }, status=400
        )

    @method_decorator(secure_required)
    def email_confirm(self, request: HttpRequest, confirmation_key: str):
        """Confirms an email address with a confirmation key."""
        userena_manager = cast(UserenaManager, UserenaSignup.objects)
        user = cast(User, userena_manager.confirm_email(confirmation_key))

        if user:
            if userena_settings.USERENA_USE_MESSAGES:
                messages.success(
                    request,
                    XtraderResponseMessages.EMAIL_CHANGE_SUCCESS,
                    fail_silently=True,
                )

            redirect_to = reverse(
                AccountsURLS.EMAIL_CHANGE_COMPLETED,
                kwargs={XtraderRequestKeys.USERNAME: user.username},
            )
            return redirect(redirect_to)
        return render(
            request=request,
            template_name=AccountsTemplates.USERENA_EMAIL_CHANGE_COMPLETED,
            context={},
        )


authentication_views = AuthenticationViews()
