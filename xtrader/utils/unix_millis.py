from typing import Optional
from datetime import datetime, timezone, date

class UnixMillis:
    "Converts datetime to milliseconds passed since  Unix Time start aka Timestamp."
    @classmethod
    def from_dt_to_ms(cls, dt: Optional[datetime] = None) -> int|None:
        if dt is None:
            return None
        return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)
    
    @classmethod
    def from_ms_to_s(cls, ms: int) -> int:
        return ms // 1000

    @classmethod
    def from_ms_to_dt(cls, ms: int) -> datetime:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)

    @classmethod
    def normalize_to_milli_second(cls, ts_ms: int) -> int:
        return (ts_ms // 1000) * 1000
    
    @classmethod
    def from_date_to_ms(cls, d: Optional[date] = None) -> int | None:
        """Convert a date to milliseconds since Unix epoch."""
        if d is None:
            return None
        dt = datetime.combine(d, datetime.min.time(), tzinfo=timezone.utc)
        return cls.from_dt_to_ms(dt)
