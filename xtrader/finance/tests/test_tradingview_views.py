import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.conf import settings

from finance.views import TradingViewIntegrationView, TradingViewWebhookView
from finance.models import TradingViewIntegration
from utils.consts import XtraderResponseKeys, XtraderResponseMessages
from accounts.exceptions import NoProfileFoundForUser
from finance.exceptions import NoConnectedExchangeException, NoConnectedTelegramException

@pytest.mark.django_db
class TestTradingViewViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="pass")
        settings.WEBHOOK_URL_TEMPLATE = "https://example.com/webhook/{}"

    @patch("finance.views.tradingview_views.generate_secure_token", return_value="securetoken")
    def test_tradingview_integration_get(self, mock_token):
        request = self.rf.get("/tradingview-integration/")
        request.user = self.user

        with patch.object(TradingViewIntegration.objects, "get_or_create") as mock_get_or_create:
            integration = MagicMock()
            integration.webhook_token = "securetoken"
            integration.auto_trading_enabled = True
            integration.telegram_notifications_enabled = False
            mock_get_or_create.return_value = (integration, True)

            response = TradingViewIntegrationView.as_view()(request)
            assert response.status_code == 200
            data = json.loads(response.content.decode())
            assert data[XtraderResponseKeys.WEBHOOK] == "https://example.com/webhook/securetoken"
            assert data[XtraderResponseKeys.TRADING] is True
            assert data[XtraderResponseKeys.NOTIFICATION] is False

    def test_tradingview_integration_post_success(self):
        request = self.rf.post("/tradingview-integration/", content_type="application/json")
        request.user = self.user
        body_data = {XtraderResponseKeys.TRADING: True, XtraderResponseKeys.NOTIFICATION: False}
        request._body = json.dumps(body_data).encode()

        with patch.object(TradingViewIntegration.objects, "get") as mock_get:
            integration = MagicMock()
            integration.webhook_token = "token"
            integration.auto_trading_enabled = True
            integration.telegram_notifications_enabled = False
            integration.update_settings = MagicMock()
            mock_get.return_value = integration

            response = TradingViewIntegrationView.as_view()(request)
            assert response.status_code == 200
            data = json.loads(response.content.decode())
            assert data[XtraderResponseKeys.WEBHOOK] == "https://example.com/webhook/token"
            assert data[XtraderResponseKeys.TRADING] is True
            assert data[XtraderResponseKeys.NOTIFICATION] is False

    def test_tradingview_integration_post_not_found(self):
        request = self.rf.post("/tradingview-integration/", content_type="application/json")
        request.user = self.user
        request._body = json.dumps({}).encode()

        with patch.object(TradingViewIntegration.objects, "get") as mock_get:
            mock_get.side_effect = TradingViewIntegration.DoesNotExist

            response = TradingViewIntegrationView.as_view()(request)
            assert response.status_code == 404
            data = json.loads(response.content.decode())
            assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.TRADING_VIEW_NOT_FOUND

    def test_tradingview_integration_post_exceptions(self):
        request = self.rf.post("/tradingview-integration/", content_type="application/json")
        request.user = self.user
        request._body = json.dumps({}).encode()

        # Test JSON decode error
        with patch.object(TradingViewIntegration.objects, "get") as mock_get:
            integration = MagicMock()
            integration.update_settings.side_effect = json.JSONDecodeError("msg", "doc", 0)
            mock_get.return_value = integration

            response = TradingViewIntegrationView.as_view()(request)
            assert response.status_code == 400
            data = json.loads(response.content.decode())
            assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.SOMETHING_WENT_WRONG

        # Test NoProfileFoundForUser
        with patch.object(TradingViewIntegration.objects, "get") as mock_get:
            integration = MagicMock()
            integration.update_settings.side_effect = NoProfileFoundForUser
            mock_get.return_value = integration
            response = TradingViewIntegrationView.as_view()(request)
            data = json.loads(response.content.decode())
            assert response.status_code == 400
            assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.NO_PROFILE_FOR_USER

        # Test NoConnectedExchangeException
        with patch.object(TradingViewIntegration.objects, "get") as mock_get:
            integration = MagicMock()
            integration.update_settings.side_effect = NoConnectedExchangeException
            mock_get.return_value = integration
            response = TradingViewIntegrationView.as_view()(request)
            data = json.loads(response.content.decode())
            assert response.status_code == 400
            assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.CONNECTED_EXCHANGE_REQUIRED_FOR_TRADING_VIEW_AUTO_TRADE

        # Test NoConnectedTelegramException
        with patch.object(TradingViewIntegration.objects, "get") as mock_get:
            integration = MagicMock()
            integration.update_settings.side_effect = NoConnectedTelegramException
            mock_get.return_value = integration
            response = TradingViewIntegrationView.as_view()(request)
            data = json.loads(response.content.decode())
            assert response.status_code == 400
            assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.CONNECTED_TELEGRAM_REQUIRED_FOR_TELEGRAM_NOTIFICATION

    def test_tradingview_webhook_get(self):
        request = self.rf.get("/tradingview-webhook/token123")
        response = TradingViewWebhookView.as_view()(request, "token123")
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.RAMZ_E_SERVAT] == XtraderResponseMessages.TRADING_VIEW_WEBHOOK_WORKS

    def test_tradingview_webhook_post_success(self):
        request = self.rf.post("/tradingview-webhook/token123")
        request.user = self.user
        request._body = b'{"key":"value"}'

        with patch("finance.views.tradingview_views.TradingViewService") as mock_service_cls:
            service = MagicMock()
            service.handle_webhook.return_value = {"ok": True}
            mock_service_cls.return_value = service

            response = TradingViewWebhookView.as_view()(request, "token123")
            assert response.status_code == 200
            data = json.loads(response.content.decode())
            assert data == {"ok": True}

    def test_tradingview_webhook_post_exceptions(self):
        request = self.rf.post("/tradingview-webhook/token123")
        request.user = self.user
        request._body = b'{}'

        # TradingViewIntegration.DoesNotExist
        with patch("finance.views.tradingview_views.TradingViewService") as mock_service_cls:
            service = MagicMock()
            service.handle_webhook.side_effect = TradingViewIntegration.DoesNotExist
            mock_service_cls.return_value = service
            response = TradingViewWebhookView.as_view()(request, "token123")
            assert response.status_code == 404

        # NoConnectedExchangeException
        with patch("finance.views.tradingview_views.TradingViewService") as mock_service_cls:
            service = MagicMock()
            service.handle_webhook.side_effect = NoConnectedExchangeException
            mock_service_cls.return_value = service
            response = TradingViewWebhookView.as_view()(request, "token123")
            assert response.status_code == 400

        # NoConnectedTelegramException
        with patch("finance.views.tradingview_views.TradingViewService") as mock_service_cls:
            service = MagicMock()
            service.handle_webhook.side_effect = NoConnectedTelegramException
            mock_service_cls.return_value = service
            response = TradingViewWebhookView.as_view()(request, "token123")
            assert response.status_code == 400

        # Generic Exception
        with patch("finance.views.tradingview_views.TradingViewService") as mock_service_cls:
            service = MagicMock()
            service.handle_webhook.side_effect = Exception("fail")
            mock_service_cls.return_value = service
            response = TradingViewWebhookView.as_view()(request, "token123")
            assert response.status_code == 500
