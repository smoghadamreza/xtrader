from django.contrib.auth import views as auth_views
from django.urls import re_path, reverse_lazy
from userena import settings as userena_settings

from utils.templates import TextTemplates
from accounts.templates import AccountsTemplates
import accounts.views as userena_views
from accounts.views import (
    authentication_views,
    profile_views,
    wallet_views,
    ProfileListView,
)


urlpatterns = [
    re_path(r"^new-deposit/$", wallet_views.new_deposit, name="new-deposit"),
    re_path(r"^get-wallet/$", wallet_views.get_wallet_snapshot, name="get-wallet"),
    re_path(
        r"^sync-deposits/$", wallet_views.sync_deposits, name="sync-deposits"
    ),
    re_path(r"^get-deposits/$", wallet_views.get_deposits, name="get-deposits"),
    re_path(r"^sign-up/$", authentication_views.sign_up, name="userena-sign-up"),
    re_path(r"^sign-in/$", authentication_views.sign_in, name="userena-sign-in"),
    re_path(
        r"^sign-out/$",
        authentication_views.sign_out,
        name="userena-sign-out",
    ),
    re_path(
        r"^confirm-email/(?P<confirmation_key>\w+)/$",
        authentication_views.email_confirm,
        name="userena-email-confirm",
    ),
        re_path(
        r"^activate/(?P<activation_key>\w+)/$",
        authentication_views.activate,
        name="userena-activate",
    ),
    re_path(
        r"^activate/retry/(?P<activation_key>\w+)/$",
        authentication_views.activate_retry,
        name="userena-retry-activation",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/pending/$",
        authentication_views.activate_pending,
        name="userena-activation-pending",
    ),
    re_path(
        r"^(?P<username>[\@\.\w-]+)/password/reset/$",
        auth_views.PasswordResetView.as_view(
            template_name=AccountsTemplates.USERENA_FORGOT_PASSWORD_FORM,
            email_template_name=TextTemplates.USERENA_EMAIL_PASSWORD_CHANGE_MESSAGE_TXT,
            extra_context={
                "without_usernames": userena_settings.USERENA_WITHOUT_USERNAMES,
            },
            success_url=reverse_lazy("accounts:userena-password-reset-done"),
        ),
        name="userena-password-reset",
    ),
    re_path(
        r"^password/reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$",
        auth_views.PasswordResetConfirmView.as_view(
            template_name=AccountsTemplates.USERENA_PASSWORD_CHANGE_CONFIRMATION_FORM,
            success_url=reverse_lazy("userena-password-reset-complete"),
        ),
        name="userena-password-reset-confirm",
    ),
    re_path(
        r"^password/reset-done/$",
        auth_views.PasswordResetDoneView.as_view(
            template_name=AccountsTemplates.USERENA_PASSWORD_CHANGE_VERIFICATION
        ),
        name="userena-password-reset-done",
    ),
    re_path(
        r"^password/reset-completed/$",
        auth_views.PasswordResetCompleteView.as_view(
            template_name=AccountsTemplates.USERENA_PASSWORD_CHANGE_COMPLETED
        ),
        name="userena-password-reset-completed",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/email-change/$",
        profile_views.change_email,
        name="userena-email-change",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/sign-up/completed/$",
        profile_views.sign_up_completed,
        name="userena-sign-up-completed",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/email-change-completed/$",
        profile_views.email_change_completed,
        name="userena-email-change-completed",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/email-change-verification-needed/$",
        profile_views.email_change_verification_needed,
        name="userena-email-change-verification-needed",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/disabled/$",
        profile_views.account_is_disabled,
        name="userena-account-disabled",
    ),
    re_path(
        r"^(?P<username>[\@\.\+\w-]+)/edit/$",
        profile_views.edit_profile,
        name="userena-profile-edit",
    ),
    re_path(
        r"^(?P<username>(?!(sign-out|sign-up|sign-in)/)[\@\.\+\w-]+)/$",
        profile_views.profile_detail,
        name="userena-profile-detail",
    ),
    re_path(
        r"^telegram-webhook", profile_views.telegram_webhook, name="telegram-webhook"
    ),
    re_path(r"^telegram-status/$", profile_views.telegram_status, name="telegram-status"),
    re_path(r"^account-status", profile_views.profile_status, name="account-status"),
    re_path(
        r"^(?:page/(?P<page>[0-9]+)/)?$",
        ProfileListView.as_view(),
        name="userena-profile-list",
    ),
]
