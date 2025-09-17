# accounts/services/notification_service.py
from django.conf import settings
import requests

class NotificationService:
    @staticmethod
    def send_telegram_message(message: str, chat_id: int) -> bool:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(send_url, data=data)
        return response.status_code == 200

    @staticmethod
    def send_deposit_notification(init_amount: float, final_amount: float) -> None:
        message = f"New deposit: Initial {init_amount}, Final {final_amount}"
        # You might want to get chat_id from settings or database
        NotificationService.send_telegram_message(message, 121366977)
