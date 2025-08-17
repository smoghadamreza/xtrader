from datetime import timedelta
from django.utils import timezone

from finance.models import StockWatch
from .unix_millis import UnixMillis

class MarketChecker:
    """
    Utility class to check market status, market time, and historical data updates.
    """

    THURSDAY = 3
    FRIDAY = 4

    MARKET_OPEN_HOUR = 8
    MARKET_OPEN_MINUTE = 30
    MARKET_CLOSE_HOUR = 12
    MARKET_CLOSE_MINUTE = 30

    def __init__(self):
        self.current_time = timezone.now()

    def is_market_day(self) -> bool:
        """
        Returns True if today is a market day (not Thursday or Friday).
        """
        return self.current_time.weekday() not in {self.THURSDAY, self.FRIDAY}

    def is_market_open(self) -> bool:
        """
        Checks if we are on market hours.
        """
        market_open = self.current_time.replace(
            hour=self.MARKET_OPEN_HOUR, minute=self.MARKET_OPEN_MINUTE
        )
        market_close = self.current_time.replace(
            hour=self.MARKET_CLOSE_HOUR, minute=self.MARKET_CLOSE_MINUTE
        )
        return (
            self.current_time > market_open and
            self.current_time < market_close
        )

    def get_last_market_date(self) -> str:
        """
        Retrieves the last available market date from the StockWatch table.
        """
        last_record = StockWatch.objects.order_by("-last_trade_date").first()
        if not last_record:
            raise ValueError("No stock market data found in the database.")
        return UnixMillis.format_date_to_str(last_record.last_trade_date)

    def find_recent_market_day(self) -> str | None:
        """
        Finds the most recent market day within the past 10 days.
        """
        for delta_days in range(10):
            date_str = UnixMillis.format_date_to_str(
                dt=self.current_time - timedelta(days=delta_days)
            )
            if StockWatch.objects.filter(last_trade_date=date_str).exists():
                return date_str
        return None
