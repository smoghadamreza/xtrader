class NoConnectedExchangeException(Exception):
    """Exception raised for invalid user input."""
    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message) # Call parent constructor with the message
