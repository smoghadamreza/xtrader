from dataclasses import dataclass
from typing import Any, Dict

from finance.exchange.constants.binance import BinanceResponseKeys


@dataclass
class AssetBalance:
    """
    Represents the available and locked balance of an asset in a Binance wallet.

    Fields:
    - symbol: The asset symbol (e.g., BTC, ETH)
    - free: Amount of the asset freely available for trading
    - locked: Amount of the asset currently locked (e.g., in orders)

    This is useful for:
    - Displaying user wallet status
    - Validating sufficient balance before placing trades
    - Monitoring changes in balance after trade execution
    """

    symbol: str
    free: float
    locked: float

    @classmethod
    def loads(cls, balance: Dict[str, Any]) -> "AssetBalance":
        return cls(
            symbol=balance[BinanceResponseKeys.ASSET],
            free=float(balance[BinanceResponseKeys.FREE]),
            locked=float(balance[BinanceResponseKeys.LOCKED])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            BinanceResponseKeys.SYMBOL: self.symbol,
            BinanceResponseKeys.FREE: self.free,
            BinanceResponseKeys.LOCKED: self.locked
        }