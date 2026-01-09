import threading
from typing import cast

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from utils.consts import XtraderResponseKeys, XtraderRequestKeys
from accounts.services import (
    WalletService, DepositService, NotificationService
)
from accounts.exceptions import NoWalletFoundForUser
from accounts.services.data import DepositCreationParams
from utils.consts import XtraderResponseMessages, XtraderResponseKeys

class WalletViews:
    """Class to group all wallet and deposit related views."""

    @method_decorator(require_POST)
    @method_decorator(csrf_exempt)
    @method_decorator(transaction.atomic)
    def new_deposit(self, request: HttpRequest) -> JsonResponse:
        """Create a new deposit."""
        nonce = request.GET.get(XtraderRequestKeys.NONCE, None)
        params = DepositCreationParams.from_dict(
            data=request.POST.dict()
        )
        _, created = DepositService.get_or_create_deposit(
            params=params,
            wallet_nonce=nonce
        )
        if created:
            t = threading.Thread(
                target=NotificationService.send_deposit_notification,
                args=(params.init_amount, params.final_amount)
            )
            t.start()
        return JsonResponse({XtraderResponseKeys.M: created})

    @method_decorator(require_GET)
    @method_decorator(login_required)
    def get_wallet_snapshot(self, request: HttpRequest) -> JsonResponse:
        """Get wallet snapshot for the user."""
        user = cast(User, request.user)
        wallet_service = WalletService.from_user(
            user=user,
            create_wallet_if_not_exists=True
        )
        wallet_snapshot = wallet_service.get_wallet_snapshot()
        snapshot_data = wallet_snapshot.to_dict()
        snapshot_data[XtraderResponseKeys.STATUS] = \
            200 if wallet_snapshot.address else 505
        return JsonResponse(data=snapshot_data)

    @method_decorator(require_GET)
    @method_decorator(login_required)
    def sync_deposits(self, request: HttpRequest) -> JsonResponse:
        """Check for new deposits for the user."""
        try:
            user = cast(User, request.user)
            wallet_service = WalletService.from_user(user=user, create_wallet_if_not_exists=False)
            fetched_new_deposits = wallet_service.fetch_and_create_new_deposits()
            return JsonResponse(
                {
                    XtraderResponseKeys.STATUS: 200,
                    XtraderResponseKeys.NEW_DEPOSIT: fetched_new_deposits
                }
            )
        except NoWalletFoundForUser:
            return JsonResponse(
                {
                    XtraderResponseKeys.STATUS: 403,
                    XtraderResponseKeys.MESSAGE: XtraderResponseMessages.NO_WALLET_FOR_USER
                }
            )

    @method_decorator(require_GET)
    @method_decorator(login_required)
    def get_deposits(self, request: HttpRequest) -> JsonResponse:
        """Get all deposits for the user."""
        user = cast(User, request.user)
        wallet_service = WalletService.from_user(user=user)
        deposits = DepositService.get_deposits(
            wallet=wallet_service.wallet
        )
        return JsonResponse({XtraderResponseKeys.DATA: deposits})

wallet_views = WalletViews()
