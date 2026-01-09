
from typing import cast, Union, Dict, Any, Type

from dataclasses import dataclass
from finance.services.exchange.constants.binance import BinanceResponseKeys

@dataclass
class DepositRecord:
    """
    Represents a deposit record from Binance deposit history endpoint.

    Fields:
    - deposit_id: Unique identifier for the deposit
    - asset_symbol: The asset symbol deposited (e.g., BTC, USDT)
    - deposit_amount: The amount deposited
    - deposit_address: The address to which deposit was sent
    - transaction_id: Blockchain transaction ID for the deposit
    - deposit_status: Status code of the deposit
    - insert_time_ms: Time the deposit was inserted (timestamp in milliseconds)
    - confirm_times: Number of confirmations required
    - address_tag: Optional address tag or memo (if applicable)
    """

    deposit_id: int
    asset_symbol: str
    deposit_amount: float
    deposit_address: str
    transaction_id: str
    deposit_status: int
    insert_time_ms: int
    confirm_times: str
    address_tag: str

    @classmethod
    def loads(cls, deposit: Dict[str, Any]) -> "DepositRecord":
        return cls(
            deposit_id=int(deposit[BinanceResponseKeys.ID]),
            asset_symbol=deposit[BinanceResponseKeys.ASSET],
            deposit_amount=float(deposit[BinanceResponseKeys.AMOUNT]),
            deposit_address=deposit[BinanceResponseKeys.ADDRESS],
            transaction_id=deposit[BinanceResponseKeys.TRANSACTION_ID],
            deposit_status=int(deposit[BinanceResponseKeys.STATUS]),
            insert_time_ms=int(deposit[BinanceResponseKeys.INSERT_TIME]),
            confirm_times=deposit[BinanceResponseKeys.CONFIRM_TIMES],
            address_tag=deposit.get(BinanceResponseKeys.ADDRESS_TAG, "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            BinanceResponseKeys.ID: self.deposit_id,
            BinanceResponseKeys.ASSET: self.asset_symbol,
            BinanceResponseKeys.AMOUNT: self.deposit_amount,
            BinanceResponseKeys.ADDRESS: self.deposit_address,
            BinanceResponseKeys.TRANSACTION_ID: self.transaction_id,
            BinanceResponseKeys.STATUS: self.deposit_status,
            BinanceResponseKeys.INSERT_TIME: self.insert_time_ms,
            BinanceResponseKeys.CONFIRM_TIMES: self.confirm_times,
            BinanceResponseKeys.ADDRESS_TAG: self.address_tag,
        }


@dataclass
class WithdrawalRecord:
    """
    Represents a withdrawal record from Binance withdrawal history endpoint.

    Fields:
    - withdrawal_id: Unique identifier for the withdrawal
    - asset_symbol: The asset symbol withdrawn (e.g., BTC, USDT)
    - withdrawal_amount: The amount withdrawn
    - transaction_fee: The fee charged for the withdrawal
    - withdrawal_address: The address the funds were sent to
    - network: Blockchain network used for withdrawal
    - transaction_id: Blockchain transaction ID
    - withdrawal_status: Status code of the withdrawal
    - apply_time_str: Timestamp as string when the withdrawal was requested
    - transfer_type: Indicates internal transfer (0 = external, 1 = internal)
    """

    withdrawal_id: str
    asset_symbol: str
    withdrawal_amount: float
    transaction_fee: float
    withdrawal_address: str
    network: str
    transaction_id: str
    withdrawal_status: int
    apply_time_ms: int
    transfer_type: int

    @classmethod
    def loads(cls, withdrawal: Dict[str, Any]) -> "WithdrawalRecord":
        return cls(
            withdrawal_id=withdrawal[BinanceResponseKeys.ID],
            asset_symbol=withdrawal[BinanceResponseKeys.COIN],
            withdrawal_amount=float(withdrawal[BinanceResponseKeys.AMOUNT]),
            transaction_fee=float(withdrawal[BinanceResponseKeys.TRANSACTION_FEE]),
            withdrawal_address=withdrawal[BinanceResponseKeys.ADDRESS],
            network=withdrawal[BinanceResponseKeys.NETWORK],
            transaction_id=withdrawal[BinanceResponseKeys.TRANSACTION_ID],
            withdrawal_status=int(withdrawal[BinanceResponseKeys.STATUS]),
            apply_time_ms=withdrawal[BinanceResponseKeys.APPLY_TIME],
            transfer_type=int(withdrawal[BinanceResponseKeys.TRANSFER_TYPE]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            BinanceResponseKeys.ID: self.withdrawal_id,
            BinanceResponseKeys.COIN: self.asset_symbol,
            BinanceResponseKeys.AMOUNT: self.withdrawal_amount,
            BinanceResponseKeys.TRANSACTION_FEE: self.transaction_fee,
            BinanceResponseKeys.ADDRESS: self.withdrawal_address,
            BinanceResponseKeys.NETWORK: self.network,
            BinanceResponseKeys.TRANSACTION_ID: self.transaction_id,
            BinanceResponseKeys.STATUS: self.withdrawal_status,
            BinanceResponseKeys.APPLY_TIME: self.apply_time_ms,
            BinanceResponseKeys.TRANSFER_TYPE: self.transfer_type,
        }

@dataclass
class TransactionRecord:
    record_type: Type[Union[DepositRecord, WithdrawalRecord]]
    amount: float
    time: int
    metadata: Union[DepositRecord, WithdrawalRecord]

    @classmethod
    def loads(cls, record: Union[DepositRecord, WithdrawalRecord]) -> "TransactionRecord":
        if hasattr(record, "insert_time_ms"):
            deposit = cast(DepositRecord, record)
            return cls(
                record_type=DepositRecord,
                amount=deposit.deposit_amount,
                time=deposit.insert_time_ms,
                metadata=deposit
            )
        elif hasattr(record, "apply_time_ms"):
            # Convert string timestamp to milliseconds if needed
            withdrawal = cast(WithdrawalRecord, record)
            return cls(
                record_type=WithdrawalRecord,
                amount=withdrawal.withdrawal_amount,
                time=withdrawal.apply_time_ms,
                metadata=withdrawal
            )
        else:
            raise TypeError("Unsupported record type for TransactionRecord")
