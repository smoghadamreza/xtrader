from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class WalletAddressCreationResponse:
    """Represents the response after creating a wallet address."""
    status: str
    address_in: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "WalletAddressCreationResponse":
        return cls(
            status=data.get("status", "error"),
            address_in=data.get("address_in"),
            error=data.get("error"),
        )

    def to_dict(self) -> dict:
        return asdict(self)
    

@dataclass(frozen=True)
class WalletAddressCreationRequestParam:
    """Represents the request after creating a wallet address."""
    address: str
    callback: str
    priority: str
    post: int

    @classmethod
    def create(cls, usdt_wallet_url: str, callback_url: str) -> "WalletAddressCreationRequestParam":
        return cls(
            address= usdt_wallet_url,
            callback= callback_url,
            priority= "economic",
            post= 1,
        )

    def to_dict(self) -> dict:
        return asdict(self)
