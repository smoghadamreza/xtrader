import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.http import Http404
from django.test import RequestFactory
from django.contrib.auth import get_user_model

from accounts.views import (
    ExtraContextTemplateView,
    ProfileListView,
    signup,
    activate,
    activate_pending,
    activate_retry,
)
from userena import settings as userena_settings


pytestmark = pytest.mark.django_db


# ------------------------------------------------------------
# ExtraContextTemplateView
# ------------------------------------------------------------
class TestExtraContextTemplateView:
    def test_extra_context_added(self):
        rf = RequestFactory()
        request = rf.get("/dummy/")
        view = ExtraContextTemplateView.as_view(
            template_name="dummy.html", extra_context={"foo": "bar"}
        )
        response = view(request)
        assert response.status_code == 200


# ------------------------------------------------------------
# ProfileListView
# ------------------------------------------------------------
class TestProfileListView:
    def test_profile_list_view_disabled_for_nonstaff(self, django_user_model):
        rf = RequestFactory()
        user = django_user_model.objects.create_user("user1", "u1@test.com", "pwd")
        request = rf.get("/profiles/")
        request.user = user

        view = ProfileListView()
        view.request = request

        userena_settings.USERENA_DISABLE_PROFILE_LIST = True
        with pytest.raises(Http404):
            view.get_context_data()
        userena_settings.USERENA_DISABLE_PROFILE_LIST = False


# ------------------------------------------------------------
# Signup
# ------------------------------------------------------------
class TestSignupView:
    def test_signup_get_renders_form(self, client):
        url = reverse("accounts:signup")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    @patch("accounts.views.SignupFormExtra")
    def test_signup_post_valid(self, MockForm, client):
        mock_form = MagicMock()
        mock_user = get_user_model().objects.create_user(
            "newuser", "new@test.com", "pwd"
        )
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = mock_user
        MockForm.return_value = mock_form

        url = reverse("accounts:signup")
        response = client.post(url, data={"username": "newuser"})
        assert response.status_code == 302
        assert "newuser" in response.url

    @patch("accounts.views.SignupFormExtra")
    def test_signup_post_invalid(self, MockForm, client):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = False
        MockForm.return_value = mock_form

        url = reverse("accounts:signup")
        response = client.post(url, data={})
        assert response.status_code == 200
        assert "form" in response.context


# ------------------------------------------------------------
# Activate
# ------------------------------------------------------------
class TestActivateView:
    @patch("accounts.views.UserenaSignup.objects.activate_user")
    @patch("accounts.views.UserenaSignup.objects.check_expired_activation")
    def test_activate_success(
        self, mock_check_expired, mock_activate, client, django_user_model
    ):
        user = django_user_model.objects.create_user(
            "actuser", "act@test.com", "pwd"
        )
        mock_check_expired.return_value = False
        mock_activate.return_value = user

        url = reverse("accounts:activate", args=["validkey"])
        response = client.get(url)
        assert response.status_code == 200 or response.status_code == 302

    @patch("accounts.views.UserenaSignup.objects.activate_user")
    @patch("accounts.views.UserenaSignup.objects.check_expired_activation")
    def test_activate_invalid_key(
        self, mock_check_expired, mock_activate, client
    ):
        mock_check_expired.return_value = False
        mock_activate.return_value = None

        url = reverse("accounts:activate", args=["badkey"])
        response = client.get(url)
        assert response.status_code == 400
        assert b"invalid link" in response.content


# ------------------------------------------------------------
# Activate Pending
# ------------------------------------------------------------
class TestActivatePendingView:
    def test_user_not_active_pending(self, django_user_model, client):
        user = django_user_model.objects.create_user(
            "pendinguser", "pending@test.com", "pwd", is_active=False
        )
        # attach a fake userena_signup object
        user.userena_signup = MagicMock(activation_completed=False)

        url = reverse("accounts:activate_pending", args=[user.username])
        response = client.get(url)
        assert response.status_code == 200


# ------------------------------------------------------------
# Activate Retry
# ------------------------------------------------------------
class TestActivateRetryView:
    @patch("accounts.views.UserenaSignup.objects.check_expired_activation")
    @patch("accounts.views.UserenaSignup.objects.reissue_activation")
    def test_retry_success(
        self, mock_reissue, mock_check_expired, client
    ):
        mock_check_expired.return_value = True
        mock_reissue.return_value = "newkey"

        url = reverse("accounts:activate_retry", args=["expiredkey"])
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == {}

    @patch("accounts.views.UserenaSignup.objects.check_expired_activation")
    def test_retry_non_expired(self, mock_check_expired, client):
        mock_check_expired.return_value = False

        url = reverse("accounts:activate_retry", args=["activekey"])
        response = client.get(url)
        assert response.status_code == 400
        assert "activation link has not expired" in response.json()["msg"]
