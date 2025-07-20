from typing import Optional
from datetime import datetime, timezone

class UnixMillis:
    "Converts datetime to milliseconds passed since  Unix Time start aka Timestamp."
    @classmethod
    def to_ms(cls, dt: Optional[datetime] = None) -> int|None:
        if dt is None:
            return None
        return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

    @classmethod
    def from_ms(cls, ms: int) -> datetime:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
