import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404, JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm

from accounts.views.profile_views import profile_views
from utils.consts import (
    XtraderResponseMessages,
    XtraderResponseKeys,
)
from accounts.url_names import AccountsURLS
from accounts.models import Profile
from accounts.exceptions import NoProfileFoundForUser


@pytest.mark.django_db
class TestAccountIsDisabled:
    @patch("accounts.views.profile_views.render")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    def test_disabled_user_renders_template(self, mock_get_user_profile: MagicMock, mock_render: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.ACCOUNT_DISABLED, kwargs={"username": "disabled"}))
        user = User(username="disabled", is_active=False)
        profile = MagicMock()
        mock_get_user_profile.return_value = (user, profile)
        mock_render.return_value = HttpResponse("ok")

        response = profile_views.account_is_disabled(request, "disabled")
        assert response.status_code == 200
        context = mock_render.call_args[1]["context"]
        assert context["profile"] == profile

    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    def test_active_user_raises_404(self, mock_get_user_profile: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.ACCOUNT_DISABLED, kwargs={"username": "active"}))
        user = User(username="active", is_active=True)
        mock_get_user_profile.return_value = (user, MagicMock())

        with pytest.raises(Http404):
            profile_views.account_is_disabled(request, "active")


@pytest.mark.django_db
class TestEditProfile:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="puser", password="pass")
        self.profile = Profile.objects.create(user=self.user)
        assign_perm("change_profile", self.user, self.profile)

    def test_get_renders_form(self):
        request = self.rf.get(reverse(AccountsURLS.PROFILE_EDIT, kwargs={"username": self.user.username}))
        request.user = self.user
        response = profile_views.edit_profile(request, username=self.user.username)
        assert response.status_code == 200

    def test_post_updates_profile_and_redirects(self):
        request = self.rf.post(
            reverse(AccountsURLS.PROFILE_EDIT, kwargs={"username": self.user.username}),
            {
                "first_name": "John",
                "last_name": "Doe",
            }
        )
        request.user = self.user

        response = profile_views.edit_profile(request, username=self.user.username)

        assert response.status_code == 302
        assert response["Location"] == reverse(
            AccountsURLS.PROFILE_DETAIL,
            kwargs={"username": self.user.username},
        )

        self.user.refresh_from_db()
        assert self.user.first_name == "John"
        assert self.user.last_name == "Doe"


@pytest.mark.django_db
class TestProfileDetail:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="pdetail", password="pass")

    @patch("accounts.views.profile_views.render")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    @patch("accounts.views.profile_views.userena_settings")
    def test_profile_detail_renders_when_allowed(
        self, mock_settings: MagicMock, mock_get_user_profile: MagicMock, mock_render: MagicMock
    ):
        request = self.rf.get(reverse(AccountsURLS.PROFILE_DETAIL, kwargs={"username": self.user.username}))
        request.user = self.user
        profile = MagicMock()
        profile.can_view_profile.return_value = True
        mock_get_user_profile.return_value = (self.user, profile)
        mock_settings.USERENA_PROFILE_DETAIL_TEMPLATE = "template.html"
        mock_settings.USERENA_HIDE_EMAIL = True
        mock_render.return_value = HttpResponse("ok")

        response = profile_views.profile_detail(request, self.user.username)
        assert response.status_code == 200
        context = mock_render.call_args[1]["context"]
        assert context["profile"] == profile

    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    def test_profile_detail_denied_raises(self, mock_get_user_profile: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.PROFILE_DETAIL, kwargs={"username": self.user.username}))
        request.user = self.user
        profile = MagicMock()
        profile.can_view_profile.return_value = False
        mock_get_user_profile.return_value = (self.user, profile)

        with pytest.raises(PermissionDenied):
            profile_views.profile_detail(request, self.user.username)


@pytest.mark.django_db
class TestProfileStatus:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="pstatus", password="pass")

    @patch("accounts.views.profile_views.AccountStatusService.get_profile_status")
    def test_status_returns_json(self, mock_get_status: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.ACCOUNT_STATUS))
        request.user = self.user
        mock_get_status.return_value = {"status": "ok"}

        response = profile_views.profile_status(request)
        assert isinstance(response, JsonResponse)
        data = json.loads(response.content.decode())
        assert data["status"] == "ok"


@pytest.mark.django_db
class TestTelegramStatus:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="ptg", password="pass")

    @patch("accounts.views.profile_views.ProfileService")
    def test_telegram_status_success(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.TELEGRAM_STATUS))
        request.user = self.user

        service = MagicMock()
        service.has_telegram_id.return_value = True
        service.get_telegram_activation_code.return_value = "123"
        mock_service_cls.return_value = service

        response = profile_views.telegram_status(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.TELEGRAM_ID] is True
        assert data[XtraderResponseKeys.ACTIVATION_CODE] == "123"

    @patch("accounts.views.profile_views.ProfileService", side_effect=NoProfileFoundForUser)
    def test_telegram_status_no_profile(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.TELEGRAM_STATUS))
        request.user = self.user

        response = profile_views.telegram_status(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.MESSAGE] == XtraderResponseMessages.NO_PROFILE_FOR_USER


@pytest.mark.django_db
class TestChangeEmail:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="cemail", password="pass")

    @patch("accounts.views.profile_views.render")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    @patch("accounts.views.profile_views.ChangeEmailForm")
    def test_get_renders_form(self, mock_form: MagicMock, mock_get_user_profile: MagicMock, mock_render: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.EMAIL_CHANGE, kwargs={"username": self.user.username}))
        request.user = self.user
        mock_get_user_profile.return_value = (self.user, MagicMock())
        mock_render.return_value = HttpResponse("ok")

        response = profile_views.change_email(request, self.user.username)
        assert response.status_code == 200
        mock_form.assert_called_once()

    @patch("accounts.views.profile_views.reverse", return_value="/redirect-url/")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    @patch("accounts.views.profile_views.ChangeEmailForm")
    def test_post_valid_changes_email_and_redirects(
        self, mock_form: MagicMock, mock_get_user_profile: MagicMock, mock_reverse: MagicMock
    ):
        request = self.rf.post(reverse(AccountsURLS.EMAIL_CHANGE, kwargs={"username": self.user.username}),
                               data={"email": "new@email.com"})
        request.user = self.user
        mock_get_user_profile.return_value = (self.user, MagicMock())

        form_instance = mock_form.return_value
        form_instance.is_valid.return_value = True

        response = profile_views.change_email(request, self.user.username)
        assert response.status_code == 302

    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    def test_wrong_user_raises_permission_denied(self, mock_get_user_profile: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.EMAIL_CHANGE, kwargs={"username": self.user.username}))
        request.user = self.user
        other_user = User(username="other")
        mock_get_user_profile.return_value = (other_user, MagicMock())

        with pytest.raises(PermissionDenied):
            profile_views.change_email(request, other_user.username)


@pytest.mark.django_db
class TestSimpleRenders:
    @patch("accounts.views.profile_views.render")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    @patch("accounts.views.profile_views.userena_settings")
    def test_sign_up_completed_renders(self, mock_settings: MagicMock, mock_get_user_profile: MagicMock, mock_render: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.SIGNUP_COMPLETED, kwargs={"username": "done"}))
        user = User(username="done")
        mock_get_user_profile.return_value = (user, MagicMock())
        mock_settings.USERENA_ACTIVATION_REQUIRED = True
        mock_settings.USERENA_ACTIVATION_DAYS = 7
        mock_render.return_value = HttpResponse("ok")

        response = profile_views.sign_up_completed(request, "done")
        assert response.status_code == 200
        context = mock_render.call_args[1]["context"]
        assert "userena_activation_days" in context

    @patch("accounts.views.profile_views.render")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    def test_email_change_completed_renders(self, mock_get_user_profile: MagicMock, mock_render: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.EMAIL_CHANGE_COMPLETED, kwargs={"username": "done"}))
        user = User(username="done")
        mock_get_user_profile.return_value = (user, MagicMock())
        mock_render.return_value = HttpResponse("ok")

        response = profile_views.email_change_completed(request, "done")
        assert response.status_code == 200

    @patch("accounts.views.profile_views.render")
    @patch("accounts.views.profile_views.ProfileService.get_user_and_profile")
    def test_email_change_verification_needed_renders(self, mock_get_user_profile: MagicMock, mock_render: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.EMAIL_CHANGE_VERIFICATION_NEEDED, kwargs={"username": "done"}))
        user = User(username="done")
        mock_get_user_profile.return_value = (user, MagicMock())
        mock_render.return_value = HttpResponse("ok")

        response = profile_views.email_change_verification_needed(request, "done")
        assert response.status_code == 200
