from __future__ import annotations

import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from accounts.exceptions import NoProfileFoundForUser
from finance.models import TradingViewIntegration
from finance.services.tradingview_service import TradingViewService

from utils.consts import (
    XtraderResponseKeys, XtraderResponseMessages,
)
from utils.misc import generate_secure_token
from finance.exceptions import (
    NoConnectedExchangeException, NoConnectedTelegramException,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class TradingViewIntegrationView(View):
    """Manage TradingView integration settings for the current user."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Fetch integration config for current user."""
        integration, _ = TradingViewIntegration.objects.get_or_create(
            user=request.user,
            defaults={XtraderResponseKeys.WEBHOOK: generate_secure_token()},
        )
        return JsonResponse({
            XtraderResponseKeys.WEBHOOK: self._get_webhook_url(webhook_token=integration.webhook_token),
            XtraderResponseKeys.TRADING: integration.auto_trading_enabled,
            XtraderResponseKeys.NOTIFICATION: integration.telegram_notifications_enabled,
        })

    def post(self, request: HttpRequest) -> JsonResponse:
        """Update integration config for current user."""
        try:
            integration = TradingViewIntegration.objects.get(user=request.user)
            data: dict = json.loads(request.body)
            integration.update_settings(
                auto_trading_enabled=data.get(XtraderResponseKeys.TRADING, False),
                telegram_notifications_enabled=data.get(XtraderResponseKeys.NOTIFICATION, False),
            )
            return JsonResponse({
                XtraderResponseKeys.WEBHOOK: self._get_webhook_url(webhook_token=integration.webhook_token),
                XtraderResponseKeys.TRADING: integration.auto_trading_enabled,
                XtraderResponseKeys.NOTIFICATION: integration.telegram_notifications_enabled,
            })
        except TradingViewIntegration.DoesNotExist:
            return JsonResponse({XtraderResponseKeys.ERROR: XtraderResponseMessages.TRADING_VIEW_NOT_FOUND}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({XtraderResponseKeys.ERROR: XtraderResponseMessages.SOMETHING_WENT_WRONG}, status=400)
        except NoProfileFoundForUser:
            return JsonResponse({XtraderResponseKeys.ERROR: XtraderResponseMessages.NO_PROFILE_FOR_USER}, status=400)
        except NoConnectedExchangeException:
            return JsonResponse({XtraderResponseKeys.ERROR: XtraderResponseMessages.CONNECTED_EXCHANGE_REQUIRED_FOR_TRADING_VIEW_AUTO_TRADE}, status=400)
        except NoConnectedTelegramException:
            return JsonResponse({XtraderResponseKeys.ERROR: XtraderResponseMessages.CONNECTED_TELEGRAM_REQUIRED_FOR_TELEGRAM_NOTIFICATION}, status=400)
        
    @staticmethod
    def _get_webhook_url(webhook_token: str) -> str:
        return settings.WEBHOOK_URL_TEMPLATE.format(webhook_token)


@method_decorator(csrf_exempt, name="dispatch")
class TradingViewWebhookView(View):
    """Handle incoming TradingView webhook requests via token."""

    def get(self, _: HttpRequest, __: str) -> JsonResponse:
        return JsonResponse({
            XtraderResponseKeys.RAMZ_E_SERVAT: XtraderResponseMessages.TRADING_VIEW_WEBHOOK_WORKS
        })

    def post(self, request: HttpRequest, webhook_token: str) -> JsonResponse:
        try:
            service = TradingViewService(webhook_token=webhook_token)
            result = service.handle_webhook(
                request_body=request.body.decode(), 
                request_user=request.user
            )
            return JsonResponse(result)
        except TradingViewIntegration.DoesNotExist:
            return JsonResponse({XtraderResponseKeys.MESSAGE: XtraderResponseMessages.TRADING_VIEW_NOT_FOUND}, status=404)
        except NoConnectedExchangeException:
            return JsonResponse({XtraderResponseKeys.MESSAGE: XtraderResponseMessages.CONNECTED_EXCHANGE_REQUIRED_FOR_TRADING_VIEW_AUTO_TRADE}, status=400)
        except NoConnectedTelegramException:
            return JsonResponse({XtraderResponseKeys.MESSAGE: XtraderResponseMessages.CONNECTED_TELEGRAM_REQUIRED_FOR_TELEGRAM_NOTIFICATION}, status=400)
        except Exception as e:
            logger.exception("Unexpected error in TradingView webhook: %s", str(e))
            return JsonResponse({XtraderResponseKeys.MESSAGE: XtraderResponseMessages.ORDER_WAS_FAILED}, status=500)
