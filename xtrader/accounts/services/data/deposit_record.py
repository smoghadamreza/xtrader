from dataclasses import dataclass, asdict
from accounts.models import Deposit
from accounts.services.consts import DEPOSIT_PRIMARY_COIN, DEPOSIT_ACTION


@dataclass(frozen=True)
class DepositRecord:
    """Represents a normalized deposit record returned to clients/UI."""
    id: int
    amount: float
    txid: str  # Transaction ID
    time: str
    action: str       # Persian "واریز" = deposit
    coin: str         # e.g. "تتر (trc20)"

    @classmethod
    def from_deposit(cls, deposit: Deposit) -> "DepositRecord":
        return cls(
            id=deposit.pk,
            amount=deposit.init_amount,
            txid=deposit.txid_in,
            time=str(deposit.tx_time).replace("T", " "),
            action=DEPOSIT_ACTION,
            coin=DEPOSIT_PRIMARY_COIN,
        )

    def to_dict(self) -> dict:
        return asdict(self)
