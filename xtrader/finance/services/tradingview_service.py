import logging
from typing import Dict, Any

from django.contrib.auth.models import User

from accounts.models import Profile
from accounts.services.telegram_service import TelegramService
from finance.models import TradingViewIntegration

from finance.services.exchange.factory import ExchangeServiceFactory
from finance.services.exchange.data import OrderRequestData
from finance.exceptions import NoConnectedTelegramException

from utils.consts import XtraderResponseMessages

logger = logging.getLogger(__name__)


class TradingViewService:
    """Business logic for handling TradingView webhook integrations."""

    def __init__(self, webhook_token: str) -> None:
        self.integration = TradingViewIntegration.objects.get(webhook_token=webhook_token)

    def handle_webhook(self, request_body: str, request_user: User) -> Dict[str, Any]:
        """Main entry point for webhook processing."""
        logger.debug("Handling TradingView webhook for user=%s", self.integration.user)

        order_result: str = self._process_order(request_body, request_user)
        telegram_result: str = self._notify_telegram(order_result)

        return {
            "order": order_result,
            "telegram": telegram_result,
        }

    def _process_order(self, raw_message: str, request_user: User) -> str:
        """Parse webhook payload and send order via exchange service."""
        if not self.integration.auto_trading_enabled:
            return XtraderResponseMessages.AUTO_TRADING_DISABLED

        try:
            exchange_service = ExchangeServiceFactory.get_service_for_user(user=request_user)
            order_data = OrderRequestData.from_tradingview_request(raw_message)
            order_data.validate()

            result = exchange_service.send_order(order_data.to_dict())
            if result.get("error"):
                return str(result["msg"])

            return XtraderResponseMessages.ORDER_WAS_SENT_SUCCESSFULLY
        except Exception as e:
            logger.exception("Failed to process TradingView order: %s", str(e))
            return XtraderResponseMessages.ORDER_WAS_FAILED

    def _notify_telegram(self, order_result: str) -> str:
        """Send Telegram notification if enabled."""
        if not self.integration.telegram_notifications_enabled:
            return XtraderResponseMessages.TELEGRAM_WAS_NOT_NOTIFIED

        try:
            profile = Profile.objects.get(user=self.integration.user)
            telegram_service = TelegramService()
            result = telegram_service.send_message(
                chat_id=profile.telegram_id,
                text=order_result
            )
            return order_result if result.get("ok") else XtraderResponseMessages.TELEGRAM_NOTIFICATION_FAILED
        except Profile.DoesNotExist:
            raise NoConnectedTelegramException()
        except Exception as e:
            logger.exception("Failed to send Telegram notification: %s", str(e))
            return XtraderResponseMessages.TELEGRAM_NOTIFICATION_FAILED
