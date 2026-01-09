import requests
from django.conf import settings
from typing import Any, Dict


class TelegramService:
    """
    Service to handle interactions with Telegram Bot API.
    """

    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token or settings.XTREASURY_BOT
        self.api_url = f"{self.BASE_URL}{self.bot_token}/"

    def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> Dict[str, Any]:
        """
        Send a text message to a Telegram user.

        :param chat_id: Telegram user chat ID
        :param text: Message text
        :param parse_mode: Telegram parse mode (Markdown, HTML, etc.)
        :return: Telegram API response as a dictionary
        """
        url = self.api_url + "sendMessage"
        payload = {
            "chat_id": str(chat_id),
            "text": text,
            "parse_mode": parse_mode,
        }

        try:
            response = requests.get(url, params=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}
