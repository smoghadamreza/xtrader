class NoConnectedExchangeException(Exception):
    def __init__(self, message: str = "No exchange configured for this user"):
        self.message = message
        super().__init__(self.message)


class NoConnectedTelegramException(Exception):
    def __init__(self, message: str = "Telegram is not configured for this user"):
        self.message = message
        super().__init__(self.message)

class InvalidWebhookPayloadException(Exception):
    def __init__(self, message: str = "Telegram is not configured for this user"):
        self.message = message
        super().__init__(self.message)

class SubscriptionUpgradeNeededForCreatingStrategy(Exception):
    def __init__(self, message: str = "Subscription upgrade needed for creating the Strategy"):
        self.message = message
        super().__init__(self.message)

class StrategyWasNotFound(Exception):
    def __init__(self, strategy_id: str):
        self.message = f"Strategy with {strategy_id} was not found."
        super().__init__(self.message)

class RequiredKeyMissing(KeyError):
    def __init__(self, *args):
        self.message = f"Required key is missing from request data."
        super().__init__(*args)

class InvalidIndicatorType(ValueError):
    def __init__(self, *args, indicator_type: str):
        self.message = f"invalid indicator_type: {indicator_type}"
        super().__init__(*args)
