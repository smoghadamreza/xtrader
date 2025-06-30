from django.conf import settings
import requests


def send_telegram_message(msg, user_id):
    bot_token = settings.XTREASURY_BOT
    params = {
        'chat_id': str(user_id),
        'text': msg,
        'parse_mode': 'Markdown',
    }
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    return requests.get(url=url, params=params).json()
