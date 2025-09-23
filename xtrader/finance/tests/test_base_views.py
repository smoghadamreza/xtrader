import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse

from utils.consts import XtraderRequestKeys, XtraderResponseKeys

from finance.views.base_views import (
    get_user_context,
    index,
    about_us,
    ssl,
    profile_settings,
)


@pytest.mark.django_db
class TestMarketViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(
            username="john",
            first_name="John",
            last_name="Doe",
            password="12345",
        )

    def test_get_user_context_default_avatar(self):
        request = self.rf.get("/")
        request.user = self.user

        ctx = get_user_context(request)

        assert ctx[XtraderResponseKeys.NAME] == "John Doe"
        assert XtraderResponseKeys.IMAGE_URL in ctx
        assert ctx[XtraderResponseKeys.IMAGE_URL].startswith("https://")

    def test_get_user_context_custom_avatar(self):
        user = User.objects.create_user(username="hadi", password="x")
        request = self.rf.get("/")
        request.user = user

        ctx = get_user_context(request)
        assert ctx[XtraderResponseKeys.IMAGE_URL] == "/media/pictures/hadi.jpeg"

    @patch("finance.views.base_views.Profile")
    def test_index_with_referral(self, mock_profile_cls: MagicMock):
        request = self.rf.get("/", {XtraderRequestKeys.REFERRAL_CODE: "abc123"})
        request.user = self.user
        request.session = {}

        mock_profile = MagicMock()
        mock_profile.pk = 42
        mock_profile_cls.objects.filter.return_value.first.return_value = mock_profile

        response = index(request)
        assert isinstance(response, HttpResponse)
        assert request.session["ref_id"] == 42
        assert response.status_code == 200

    @patch("finance.views.base_views.Profile")
    def test_index_with_invalid_referral(self, mock_profile_cls: MagicMock):
        request = self.rf.get("/", {XtraderRequestKeys.REFERRAL_CODE: "badcode"})
        request.user = self.user
        request.session = {}

        mock_profile_cls.objects.filter.return_value.first.return_value = None

        response = index(request)
        assert isinstance(response, HttpResponse)
        assert "ref_id" not in request.session
        assert response.status_code == 200

    def test_index_without_referral(self):
        request = self.rf.get("/")
        request.user = self.user
        request.session = {}

        response = index(request)
        assert isinstance(response, HttpResponse)
        assert "ref_id" not in request.session
        assert response.status_code == 200

    def test_about_us(self):
        request = self.rf.get("/")
        request.user = self.user

        response = about_us(request)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 200

    def test_ssl_returns_token(self):
        request = self.rf.get("/")
        response = ssl(request)
        assert isinstance(response, HttpResponse)
        assert "S40flyGXu3pwdfdYzH" in response.content.decode()
        assert response.status_code == 200

    @patch("finance.views.base_views.get_user_context")
    def test_profile_settings(self, mock_user_ctx: MagicMock):
        mock_user_ctx.return_value = {XtraderResponseKeys.NAME: "John", XtraderResponseKeys.IMAGE_URL: "url"}
        request = self.rf.get("/")
        request.user = self.user

        response = profile_settings(request)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 200
        mock_user_ctx.assert_called_once_with(request)
