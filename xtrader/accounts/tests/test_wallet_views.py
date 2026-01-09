import json
from unittest.mock import patch, MagicMock
import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse

from accounts.views.wallet_views import wallet_views
from accounts.exceptions import NoWalletFoundForUser
from accounts.url_names import AccountsURLS
from utils.consts import XtraderResponseKeys, XtraderResponseMessages


@pytest.mark.django_db
class TestNewDeposit:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(
            username="walletuser", email="wallet@x.com", password="pass"
        )

    @patch("accounts.views.wallet_views.NotificationService.send_deposit_notification")
    @patch("accounts.views.wallet_views.DepositService.get_or_create_deposit")
    @patch("accounts.views.wallet_views.DepositCreationParams.from_dict")
    def test_new_deposit_created_triggers_notification(
        self, mock_from_dict: MagicMock, mock_get_or_create: MagicMock, mock_notify: MagicMock
    ):
        request = self.rf.post(reverse(AccountsURLS.NEW_DEPOSIT), data={"amount": "10"})
        request.user = self.user

        mock_params = MagicMock(init_amount=10, final_amount=9.5)
        mock_from_dict.return_value = mock_params
        mock_get_or_create.return_value = (MagicMock(), True)

        response = wallet_views.new_deposit(request)
        assert isinstance(response, JsonResponse)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.M] is True
        mock_get_or_create.assert_called_once()
        mock_notify.assert_called_once_with(mock_params.init_amount, mock_params.final_amount)

    @patch("accounts.views.wallet_views.DepositService.get_or_create_deposit")
    @patch("accounts.views.wallet_views.DepositCreationParams.from_dict")
    def test_new_deposit_not_created_returns_false(
        self, mock_from_dict: MagicMock, mock_get_or_create: MagicMock
    ):
        request = self.rf.post(reverse(AccountsURLS.NEW_DEPOSIT), data={"amount": "10"})
        request.user = self.user

        mock_from_dict.return_value = MagicMock()
        mock_get_or_create.return_value = (MagicMock(), False)

        response = wallet_views.new_deposit(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.M] is False


@pytest.mark.django_db
class TestSyncDeposits:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="walletuser3", password="pass")

    @patch("accounts.views.wallet_views.WalletService.from_user")
    def test_sync_deposits_success(self, mock_from_user: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.SYNC_DEPOSITS))
        request.user = self.user

        wallet_service = MagicMock()
        wallet_service.fetch_and_create_new_deposits.return_value = ["d1", "d2"]
        mock_from_user.return_value = wallet_service

        response = wallet_views.sync_deposits(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.STATUS] == 200
        assert data[XtraderResponseKeys.NEW_DEPOSIT] == ["d1", "d2"]

    @patch("accounts.views.wallet_views.WalletService.from_user")
    def test_sync_deposits_no_wallet_returns_403(self, mock_from_user: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.SYNC_DEPOSITS))
        request.user = self.user

        mock_from_user.side_effect = NoWalletFoundForUser()

        response = wallet_views.sync_deposits(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.STATUS] == 403
        assert data[XtraderResponseKeys.MESSAGE] == XtraderResponseMessages.NO_WALLET_FOR_USER


@pytest.mark.django_db
class TestGetDeposits:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="walletuser4", password="pass")

    @patch("accounts.views.wallet_views.DepositService.get_deposits")
    @patch("accounts.views.wallet_views.WalletService.from_user")
    def test_get_deposits_returns_list(
        self, mock_from_user: MagicMock, mock_get_deposits: MagicMock
    ):
        request = self.rf.get(reverse(AccountsURLS.GET_DEPOSITS))
        request.user = self.user

        wallet_service = MagicMock()
        wallet_service.wallet = MagicMock()
        mock_from_user.return_value = wallet_service
        mock_get_deposits.return_value = [{"id": 1, "amount": 100}]

        response = wallet_views.get_deposits(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.DATA] == [{"id": 1, "amount": 100}]
        mock_get_deposits.assert_called_once_with(wallet=wallet_service.wallet)


@pytest.mark.django_db
class TestGetWalletSnapshot:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="walletuser2", password="pass")

    @patch("accounts.views.wallet_views.WalletService.from_user")
    def test_get_wallet_snapshot_success_with_address(self, mock_from_user: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.GET_DEPOSITS))  # use GET_DEPOSITS constant just for path
        request.user = self.user

        wallet_service = MagicMock()
        wallet_snapshot = MagicMock()
        wallet_snapshot.address = "0x123"
        wallet_snapshot.to_dict.return_value = {"balance": 100}
        wallet_service.get_wallet_snapshot.return_value = wallet_snapshot
        mock_from_user.return_value = wallet_service

        response = wallet_views.get_wallet_snapshot(request)
        assert isinstance(response, JsonResponse)
        data = json.loads(response.content.decode())

        assert data["balance"] == 100
        assert data[XtraderResponseKeys.STATUS] == 200

    @patch("accounts.views.wallet_views.WalletService.from_user")
    def test_get_wallet_snapshot_no_address_sets_505(self, mock_from_user: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.GET_DEPOSITS))  # use GET_DEPOSITS constant just for path
        request.user = self.user

        wallet_service = MagicMock()
        wallet_snapshot = MagicMock()
        wallet_snapshot.address = None
        wallet_snapshot.to_dict.return_value = {"balance": 0}
        wallet_service.get_wallet_snapshot.return_value = wallet_snapshot
        mock_from_user.return_value = wallet_service

        response = wallet_views.get_wallet_snapshot(request)
        data = json.loads(response.content.decode())

        assert data["balance"] == 0
        assert data[XtraderResponseKeys.STATUS] == 505
