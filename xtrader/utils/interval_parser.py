class IntervalParser:
    @classmethod
    def parse_interval_to_seconds(cls, interval: str) -> int:
        """Convert Binance-like intervals into seconds."""
        unit = interval[-1]   # last character (m, h, d, w, M)
        value = int(interval[:-1])  # numeric part
        
        if unit == "m":  # minutes
            return value * 60
        elif unit == "h":  # hours
            return value * 3600
        elif unit == "d":  # days
            return value * 86400
        elif unit == "w":  # weeks
            return value * 7 * 86400
        elif unit == "M":  # months (approx, Binance treats as 30 days)
            return value * 30 * 86400
        else:
            raise ValueError(f"Unknown interval format: {interval}")
