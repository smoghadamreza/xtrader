from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from finance.exchange.base import BaseExchangeService
from finance.exchange.factory import ExchangeServiceFactory
from aum.models import Fund
from finance.exchange.constants.binance import BinanceRequestKeys
from xtrader.utils.consts import Symbol

class FundService:

    def __init__(self, fund_manager: User) -> None:
        try:
            self.fund = Fund.objects.get(manager=fund_manager)
        except Fund.DoesNotExist:
            raise PermissionDenied("No Fund configured for this manager.")

    @property
    def exchange_service(self) -> "BaseExchangeService":
        return ExchangeServiceFactory.get_service_for_user(
            user=self.fund.manager
        )

    def fetch_and_update_transactions(self, symbol_id: str = Symbol.USDT):  # replaces legacy Fund.get_transactions
        transactions = self.exchange_service.get_transactions(
            params={BinanceRequestKeys.ASSET: symbol_id}
        )
        self.fund.update_fund_balance(transactions=transactions)
        return transactions