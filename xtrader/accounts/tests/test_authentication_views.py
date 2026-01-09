import json
from unittest.mock import patch, MagicMock
import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from accounts.views.authentication_views import authentication_views
from accounts.services import UserActivationService
from utils.consts import XtraderResponseMessages, XtraderResponseKeys
from accounts.url_names import AccountsURLS


# Helper to add session to request
def add_session(request: HttpRequest) -> HttpRequest:
    """Attach session to a RequestFactory request."""
    def get_response(r: HttpRequest):
        return None
    middleware = SessionMiddleware(get_response)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.mark.django_db
class TestSignUp:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="a@b.com", password="pass"
        )

    @patch("accounts.views.authentication_views.SignupFormExtra")
    def test_get_signup_form_renders(self, mock_form: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.SIGN_UP))
        request.user = AnonymousUser()
        response = authentication_views.sign_up(request)
        assert response.status_code == 200
        mock_form.assert_called_once()

    @patch("accounts.views.authentication_views.userena_settings")
    @patch("accounts.views.authentication_views.SignupFormExtra")
    @patch("accounts.views.authentication_views.userena_signals.signup_complete.send")
    @patch("accounts.views.authentication_views.logout")
    @patch("accounts.views.authentication_views.authenticate")
    @patch("accounts.views.authentication_views.login")
    def test_post_valid_signup_creates_user_and_redirects(
        self,
        mock_login: MagicMock,
        mock_authenticate: MagicMock,
        mock_logout: MagicMock,
        mock_signal: MagicMock,
        mock_form: MagicMock,
        mock_settings: MagicMock,
    ):
        request = self.rf.post(
            reverse(AccountsURLS.SIGN_UP),
            data={"username": "newuser", "email": "x@y.com"},
        )
        request.user = AnonymousUser()
        add_session(request)

        mock_form.return_value.is_valid.return_value = True
        mock_form.return_value.save.return_value = self.user
        mock_authenticate.return_value = self.user

        mock_settings.USERENA_DISABLE_SIGNUP = False
        mock_settings.USERENA_SIGNIN_AFTER_SIGNUP = True
        mock_settings.USERENA_ACTIVATION_REQUIRED = False

        response = authentication_views.sign_up(request)
        assert isinstance(response, HttpResponseRedirect)
        mock_signal.assert_called_once()
        mock_login.assert_called_once()


@pytest.mark.django_db
class TestSignIn:
    @patch("accounts.views.authentication_views.AuthenticationForm")
    @patch("accounts.views.authentication_views.authenticate")
    @patch("accounts.views.authentication_views.login")
    def test_post_valid_signin_logs_in_and_redirects(
        self, mock_login: MagicMock, mock_auth: MagicMock, mock_form: MagicMock
    ):
        rf = RequestFactory()
        request = rf.post(
            reverse(AccountsURLS.SIGN_IN),
            data={"identification": "a@b.com", "password": "pass", "remember_me": False},
        )
        request.user = AnonymousUser()
        add_session(request)

        mock_form.return_value.is_valid.return_value = True
        mock_form.return_value.cleaned_data = {
            "identification": "a@b.com",
            "password": "pass",
            "remember_me": False,
        }
        mock_auth.return_value = User(username="a", is_active=True)

        response = authentication_views.sign_in(request)
        assert isinstance(response, HttpResponseRedirect)
        mock_login.assert_called_once()


@pytest.mark.django_db
class TestSignOut:
    @patch("accounts.views.authentication_views.logout")
    @patch("accounts.views.authentication_views.messages")
    def test_signout_logs_out_and_returns_json(
        self, mock_messages: MagicMock, mock_logout: MagicMock
    ):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.SIGN_OUT))
        request.user = User(username="a")
        add_session(request)

        response = authentication_views.sign_out(request)
        assert isinstance(response, JsonResponse)
        mock_logout.assert_called_once()
        mock_messages.success.assert_called_once()


@pytest.mark.django_db
class TestActivate:
    @patch.object(UserActivationService, "activate_user")
    def test_activate_success_returns_json(self, mock_activate: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.ACTIVATE, args=["key123"]))
        add_session(request)
        mock_activate.return_value = (User(username="a"), None)

        response = authentication_views.activate(request, "key123")
        assert isinstance(response, JsonResponse)

    @patch.object(UserActivationService, "activate_user")
    def test_activate_invalid_link_returns_400(self, mock_activate: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.ACTIVATE, args=["key123"]))
        add_session(request)
        mock_activate.return_value = (None, "invalid link")

        response = authentication_views.activate(request, "key123")
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.MESSAGE] == XtraderResponseMessages.ACTIVATION_LINK_INVALID
        assert response.status_code == 400


@pytest.mark.django_db
class TestActivateRetry:
    @patch("accounts.views.authentication_views.UserActivationService.reissue_activation")
    @patch("accounts.views.authentication_views.userena_settings")
    def test_retry_enabled_and_new_key_returns_json(
        self, mock_settings: MagicMock, mock_reissue: MagicMock
    ):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.ACTIVATE_RETRY, args=["key123"]))
        add_session(request)
        mock_settings.USERENA_ACTIVATION_RETRY = True
        mock_reissue.return_value = "new_key"

        response = authentication_views.activate_retry(request, "key123")
        assert isinstance(response, JsonResponse)


@pytest.mark.django_db
class TestEmailConfirm:
    @patch("accounts.views.authentication_views.UserenaSignup.objects.confirm_email")
    @patch("accounts.views.authentication_views.messages")
    def test_email_confirm_success_redirects(
        self, mock_messages: MagicMock, mock_confirm_email: MagicMock
    ):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.EMAIL_CONFIRM, args=["confkey"]))
        add_session(request)
        mock_confirm_email.return_value = User(username="a")

        response = authentication_views.email_confirm(request, "confkey")
        assert isinstance(response, HttpResponseRedirect)
        mock_messages.success.assert_called_once()

    @patch("accounts.views.authentication_views.UserenaSignup.objects.confirm_email")
    def test_email_confirm_failure_renders_template(self, mock_confirm_email: MagicMock):
        rf = RequestFactory()
        request = rf.get(reverse(AccountsURLS.EMAIL_CONFIRM, args=["confkey"]))
        add_session(request)
        mock_confirm_email.return_value = None

        response = authentication_views.email_confirm(request, "confkey")
        assert response.status_code == 200
