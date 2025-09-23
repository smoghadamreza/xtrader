import time
from typing import cast
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
import requests


from accounts.models import Wallet, Deposit
from .data import (
    WalletSnapshot, WalletAddressCreationResponse,
    WalletAddressCreationRequestParam, CryptApiLogsResponse,
    DepositCreationParams
)
from .deposit_service import DepositService


class WalletService:
    ADDRESS_CREATION_MAX_RETREIS = 3
    CRYPT_API_USDT_COIN = "trc20_usdt"

    class Endpoint:
        CRYPT_API_BASE = "https://api.cryptapi.io"
        CRYPT_API_USDT_ADDRESS_CREATE = CRYPT_API_BASE + "/trc20/usdt/create"
        CRYPT_API_USDT_LOGS = CRYPT_API_BASE + "/trc20/usdt/logs"
        CRYPT_API_CALLBACK = settings.SITE_ADDRESS + "/accounts/new-deposit"

        USDT_WALLET = settings.USDT_WALLET

    def __init__(self, wallet: Wallet) -> None:
        self._wallet = wallet

    @classmethod
    def from_user(cls, user: User, create_wallet_if_not_exists: bool = True) -> "WalletService":
        try:
            wallet = Wallet.objects.get(user=user)
            return cls(wallet)
        except Wallet.DoesNotExist:
            if create_wallet_if_not_exists:
                wallet = Wallet.objects.create(user=user)
                wallet_service = cls(wallet)
                wallet_service.create_address()
                return wallet_service
            raise 

    @property
    def wallet(self) -> Wallet:
        return self._wallet
    
    def get_wallet_snapshot(self) -> WalletSnapshot:  # replaces Wallet.get_wallet
        if self._should_regenerate_wallet_address():
            address = self.create_address()
            self.wallet.address = address
            self.wallet.updated_at = timezone.now()
            self.wallet.save(update_fields=["address"])
        return WalletSnapshot.from_wallet(wallet=self.wallet)

    def create_address(self) -> str:
        """
        Try to create a new deposit address via CryptAPI.
        Retries up to ADDRESS_CREATION_MAX_RETREIS times before failing.
        """
        old_nonce = self.wallet.nonce
        for _ in range(self.ADDRESS_CREATION_MAX_RETREIS):
            self.wallet.nonce = str(uuid4())
            self.wallet.save(update_fields=["nonce"])
            response = self._request_new_address()

            if self._is_wallet_address_created(response):
                response = cast(WalletAddressCreationResponse, response)
                return self._save_address(response)

            time.sleep(1)

        self.wallet.nonce = old_nonce
        self.wallet.save(update_fields=["nonce"])
        return ""  # All retries failed
    
    def fetch_and_create_new_deposits(self) -> bool:  # replaces legacy Wallet.check_deposit
        logs_data = requests.get(
            url=self.Endpoint.CRYPT_API_USDT_LOGS, params={
                "callback": self._crypt_api_callback_url
            }
        ).json()
        logs = CryptApiLogsResponse.from_dict(data=logs_data)
        
        deposit_created = []
        for callback_entry in logs.callbacks:
            if Deposit.objects.filter(txid_in=callback_entry.txid_in).exists():
                continue
            params = DepositCreationParams.from_cryptapi_logs_response(
                callback_entry=callback_entry,
                address_in=logs.address_in,
                address_out=logs.address_out,
                coin=self.CRYPT_API_USDT_COIN
            )
            _, created = DepositService.get_or_create_deposit(
                wallet=self.wallet,
                params=params
            )
            deposit_created.append(created)
        return any(deposit_created)
    

    def _should_regenerate_wallet_address(self) -> bool:
        """Check if address is older than 70 days."""
        return (timezone.now() - self.wallet.updated_at).days > 70


    def _request_new_address(self) -> WalletAddressCreationResponse| None:
        """Send request to CryptAPI and return the parsed JSON response."""
        try:
            response_data = requests.get(
                url=self.Endpoint.CRYPT_API_USDT_ADDRESS_CREATE,
                params=WalletAddressCreationRequestParam.create(
                    usdt_wallet_url=self.Endpoint.USDT_WALLET,
                    callback_url=self._crypt_api_callback_url
                ).to_dict(),
                timeout=10
            ).json()
            return WalletAddressCreationResponse.from_dict(data=response_data)
        except Exception:
            return None

    @staticmethod
    def _is_wallet_address_created(response: WalletAddressCreationResponse| None) -> bool:
        """Check if API response indicates success."""
        return (
            response is not None and
            response.status == "success" and
            response.address_in is not None and
            response.address_in != ""
        )

    def _save_address(self, response: WalletAddressCreationResponse) -> str:
        """Persist generated address to the wallet and return it."""
        address_in = cast(str, response.address_in)

        self.wallet.address = address_in
        self.wallet.save(update_fields=["address"])
        return self.wallet.address
    
    @property
    def _crypt_api_callback_url(self):
        return self.Endpoint.CRYPT_API_CALLBACK + f"?nonce={self.wallet.nonce}"
    