import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse

from utils.consts import XtraderResponseKeys
from finance.views.demo_views import (
    demo_test_volume,
    demo_test_api,
    DEFAULT_SYMBOL_ID,
)


@pytest.mark.django_db
class TestTestViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(
            username="john",
            first_name="John",
            last_name="Doe",
            password="test123",
        )

    @patch("finance.views.demo_views.get_user_context")
    def test_test_volume_view(self, mock_get_user_context: MagicMock):
        mock_get_user_context.return_value = {
            XtraderResponseKeys.NAME: "John Doe",
            XtraderResponseKeys.IMAGE_URL: "some_url",
        }

        request = self.rf.get("/")
        request.user = self.user

        response = demo_test_volume(request)

        assert isinstance(response, HttpResponse)
        assert response.status_code == 200

        # Check that context includes both default symbol ID and user context
        ctx = response.context_data
        assert ctx[XtraderResponseKeys.SYMBOL_ID] == DEFAULT_SYMBOL_ID
        assert ctx[XtraderResponseKeys.NAME] == "John Doe"
        assert ctx[XtraderResponseKeys.IMAGE_URL] == "some_url"

        mock_get_user_context.assert_called_once_with(request)

    def test_test_api_view(self):
        request = self.rf.get("/")
        request.user = self.user

        response = demo_test_api(request)

        assert isinstance(response, HttpResponse)
        assert response.status_code == 200

        ctx = response.context_data
        assert ctx[XtraderResponseKeys.SYMBOL_ID] == DEFAULT_SYMBOL_ID
