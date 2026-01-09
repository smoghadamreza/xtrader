import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

from django.http import HttpRequest
from utils.consts import XtraderRequestKeys


@dataclass(frozen=True)
class TelegramWebhookRequest:
    user_id: int
    text: str

    @classmethod
    def from_request(cls, request: HttpRequest) -> "TelegramWebhookRequest":
        """Parse and validate Telegram webhook request body into dataclass."""
        data: Dict[str, Any] = json.loads(request.body.decode())
        message: Dict[str, Any] = data[XtraderRequestKeys.MESSAGE]
        return cls(
            user_id=message[XtraderRequestKeys.FROM][XtraderRequestKeys.ID],
            text=message[XtraderRequestKeys.TEXT],
        )
