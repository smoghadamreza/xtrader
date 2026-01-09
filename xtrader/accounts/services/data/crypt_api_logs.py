from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass(frozen=True)
class CallbackDeliveryLog:
    """Represents a single delivery attempt log for a callback."""
    request_url: str
    responses: str
    response_status: str
    next_try: Optional[str]
    pending: int
    confirmed: int

    @classmethod
    def from_dict(cls, data: dict) -> "CallbackDeliveryLog":
        return cls(
            request_url=data["request_url"],
            responses=data["responses"],
            response_status=data["response_status"],
            next_try=data.get("next_try"),
            pending=int(data.get("pending", 0)),
            confirmed=int(data.get("confirmed", 0)),
        )


@dataclass(frozen=True)
class CallbackEntry:
    """Represents a payment callback entry from CryptAPI logs."""
    txid_in: str
    txid_out: str
    value_coin: float
    value_forwarded_coin: float
    confirmations: int
    last_update: str
    result: str
    fee_percent: float
    fee_coin: float
    logs: List[CallbackDeliveryLog] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "CallbackEntry":
        return cls(
            txid_in=data["txid_in"],
            txid_out=data["txid_out"],
            value_coin=float(data["value_coin"]),
            value_forwarded_coin=float(data["value_forwarded_coin"]),
            confirmations=int(data["confirmations"]),
            last_update=data["last_update"],
            result=data["result"],
            fee_percent=float(data["fee_percent"]),
            fee_coin=float(data["fee_coin"]),
            logs=[CallbackDeliveryLog.from_dict(log) for log in data.get("logs", [])],
        )
    
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class CryptApiLogsResponse:
    """Represents the full response returned from CryptAPI logs endpoint."""
    address_in: str
    address_out: str
    callback_url: str
    status: str
    notify_pending: bool
    notify_confirmations: int
    priority: str
    callbacks: List[CallbackEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "CryptApiLogsResponse":
        return cls(
            address_in=data["address_in"],
            address_out=data["address_out"],
            callback_url=data["callback_url"],
            status=data["status"],
            notify_pending=bool(data["notify_pending"]),
            notify_confirmations=int(data["notify_confirmations"]),
            priority=data["priority"],
            callbacks=[CallbackEntry.from_dict(cb) for cb in data.get("callbacks", [])],
        )
