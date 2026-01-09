from dataclasses import dataclass
from .crypt_api_logs import CryptApiLogsResponse, CallbackEntry


@dataclass(frozen=True)
class DepositCreationParams:
    """Represents parameters required to create a deposit record."""
    address_in: str
    address_out: str
    txid_in: str
    txid_out: str
    init_amount: float
    final_amount: float
    result: str
    coin: str
    network: str

    @classmethod
    def from_dict(cls, data: dict) -> "DepositCreationParams":
        """Build DepositCreationParams directly from a CryptAPI callback dictionary."""
        network, coin = data["coin"].split("_")

        return cls(
            address_in=data["address_in"],
            address_out=data["address_out"],
            txid_in=data["txid_in"],
            txid_out=data["txid_out"],
            init_amount=float(data["value_coin"]),
            final_amount=float(data["value_forwarded_coin"]),
            result=data["result"],
            coin=coin,
            network=network,
        )

    @classmethod
    def from_cryptapi_logs_response(
        cls, callback_entry: CallbackEntry, address_in: str,
        address_out: str, coin: str
    ) -> "DepositCreationParams":
        """Build DepositCreationParams from a parsed CryptAPI logs CallbackEntry."""
        data = callback_entry.to_dict()
        data["address_in"] = address_in
        data["address_out"] = address_out
        data["coin"] = coin
        return cls.from_dict(data=data)
