from django.conf import settings

from proxy.wrapper import requests_wrapper


def send_telegram_message(msg, user_id):
    bot_token = settings.XTREASURY_BOT
    # user_id = 121366977
    params = {
        'chat_id': str(user_id),
        'text': msg,
        'parse_mode': 'Markdown',
    }
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    return requests_wrapper(url=url, params=params, function_name=send_telegram_message.__name__)
