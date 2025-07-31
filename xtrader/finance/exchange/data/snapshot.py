from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime
from finance.exchange.constants.binance import BinanceResponseKeys

@dataclass
class SnapshotBalance:
    """
    Represents a balance item in an account snapshot. 
    It has an archival context rather than real-time AssetBalance.

    Fields:
    - asset: The asset symbol (e.g., BTC, ETH)
    - free: Freely available amount
    - locked: Amount locked in orders
    """
    asset: str
    free: float
    locked: float

    @classmethod
    def loads(cls, data: Dict[str, Any]) -> "SnapshotBalance":
        return cls(
            asset=data[BinanceResponseKeys.ASSET],
            free=float(data[BinanceResponseKeys.FREE]),
            locked=float(data[BinanceResponseKeys.LOCKED])
        )


@dataclass
class AccountSnapshot:
    """
    Represents a snapshot of the account at a specific time.

    Fields:
    - type: The account type (e.g., 'spot', 'margin', 'futures')
    - update_time: The time the snapshot was taken (as a datetime)
    - update_time_timestamp_ms:  The time the snapshot was taken (as timestamp milliseconds)
    - balances: List of asset balances at the time of the snapshot
    - total_asset_of_btc: Total value of assets expressed in BTC (spot-specific)
    """
    type: str
    update_time: datetime
    update_time_timestamp_ms: int
    balances: List[SnapshotBalance]
    total_asset_of_btc: float

    @classmethod
    def loads(cls, snapshot: Dict[str, Any]) -> "AccountSnapshot":
        data = snapshot[BinanceResponseKeys.DATA]
        return cls(
            type=snapshot[BinanceResponseKeys.TYPE],
            update_time=datetime.fromtimestamp(snapshot[BinanceResponseKeys.UPDATE_TIME] / 1000),
            update_time_timestamp_ms=snapshot[BinanceResponseKeys.UPDATE_TIME],
            balances=[SnapshotBalance.loads(b) for b in data.get(BinanceResponseKeys.BALANCES, [])],
            total_asset_of_btc=float(data.get(BinanceResponseKeys.TOTAL_ASSETS_OF_BTC, 0.0))
        )
