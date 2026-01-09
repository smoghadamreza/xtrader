import logging
from typing import Tuple, Optional, Dict, List
from django.contrib.auth.models import User

from accounts.models import Deposit, Wallet
from accounts.exceptions import NoDepositFoundForUser
from .data import DepositCreationParams, DepositRecord
from .consts import ORPHAN_DEPOSIT_ERROR_MESSAGE


logger = logging.getLogger(__name__)



class DepositService:
    def __init__(self, deposit: Deposit) -> None:
        self._deposit = deposit

    @classmethod
    def from_user(cls, user: User) -> "DepositService":
        try:
            deposit = Deposit.objects.get(user=user)
        except Deposit.DoesNotExist:
            raise NoDepositFoundForUser()
        return cls(deposit)

    @property
    def deposit(self) -> Deposit:
        return self._deposit
    

    @classmethod
    def get_or_create_deposit(
        cls, params: DepositCreationParams, wallet: Optional[Wallet] = None,
        wallet_nonce: Optional[str] = None
    ) -> Tuple[Deposit, bool]:  # replaces legacy Deposit.create
        if wallet is None:
            try:
                wallet = Wallet.objects.get(nonce=wallet_nonce, address=params.address_in)
            except Wallet.DoesNotExist:
                logger.fatal(ORPHAN_DEPOSIT_ERROR_MESSAGE)
        deposit, created = Deposit.objects.get_or_create(
            address_in=params.address_in,
            txid_in=params.txid_in,
            defaults={
                "wallet": wallet,
                "address_out": params.address_out,
                "txid_out": params.txid_out,
                "init_amount": params.init_amount,
                "final_amount": params.final_amount,
                "result": params.result,
                "coin": params.coin,
                "network": params.network,
            },
        )
        if wallet:
            # It was deposit.init_amount at first,
            # this seems correct and logical.
            wallet.balance += deposit.final_amount
            wallet.save()
        return deposit, created
    
    @classmethod
    def get_deposits(cls, wallet: Wallet) -> List[Dict[str, str|float]]:
        deposits = Deposit.objects.filter(wallet=wallet).order_by("tx_time")
        return [
            DepositRecord.from_deposit(deposit=d).to_dict() for d in deposits
        ]
