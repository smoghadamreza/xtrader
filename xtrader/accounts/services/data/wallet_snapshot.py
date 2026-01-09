from dataclasses import dataclass, asdict
from accounts.models import Wallet


@dataclass(frozen=True)
class WalletSnapshot:
    """Represents a lightweight snapshot of a wallet state."""
    address: str
    balance: float
    income: float

    @classmethod
    def from_wallet(cls, wallet: Wallet) -> "WalletSnapshot":
        return cls(
            address=wallet.address,
            balance=wallet.balance,
            income=wallet.income,
        )

    def to_dict(self) -> dict:
        return asdict(self)
