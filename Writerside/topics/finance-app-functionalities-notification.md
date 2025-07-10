# Notifications

## Core Components

### Message Delivery
- `send_telegram_message(msg, user_id)`  
   + **Purpose**: Sends formatted messages via Telegram bot  
   + **Inputs**:  
        - `msg`: `str` - Markdown-formatted message content (e.g., `'*Alert*: Price reached $50000'`)  
        - `user_id`: `int`/`str` - Recipient's Telegram identifier (e.g., `121366977`)  
   + **Output**: `dict` - Telegram API response containing:  
        - `ok`: `bool` - Success status  
        - `result`: `dict` - Message metadata including `message_id`, `chat`, and `text`  

## Configuration
- `XTREASURY_BOT`: Bot token stored in [](settings.md)

## Dependencies
- Uses <include from="third-party-libraries-links.topic" element-id="python-requests"/> for HTTP communication  
- Requires valid Telegram bot token configured in Django settings
