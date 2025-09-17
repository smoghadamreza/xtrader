import logging
from datetime import datetime, timedelta, timezone

from typing import cast, Dict, Any, List, Optional

from .authenticated_api import AuthenticatedAPIClient
from finance.services.exchange.constants.binance import BinanceRequestKeys, BinanceResponseKeys, BinanceResponseValues, BinanceRequestValues, BUYING_POWER
from finance.services.exchange.data import (
    AccountSnapshot, OrderType, DepositRecord, WithdrawalRecord,
    TransactionRecord, AssetBalance

)
from utils.unix_millis import UnixMillis

logger = logging.getLogger(__name__)


class AccountAPIClient(AuthenticatedAPIClient):

    class Endpoint:
        ACCOUNT = AuthenticatedAPIClient.V3_ENDPOINT + "/account"
        ALL_ORDERS = AuthenticatedAPIClient.V3_ENDPOINT + "/allOrders"
        OPEN_ORDERS = AuthenticatedAPIClient.V3_ENDPOINT + "/openOrders"

        # replaced by the deprected /wapi/v3/depositHistory
        DEPOSITS = AuthenticatedAPIClient.V1_ENDPOINT + "/capital/deposit/hisrec"
        # replaced by the deprecated /wapi/v3/withdrawHistory
        WITHDRAWALS = AuthenticatedAPIClient.V1_ENDPOINT + "/capital/withdraw/history"
        SNAPSHOT = AuthenticatedAPIClient.V1_ENDPOINT + "/accountSnapshot"

    def get_portfolio(self) -> List[AssetBalance]:
        """
        Fetches all non-zero asset balances in the user's wallet.
        
        Returns:
            List of dicts, each representing a non-zero balance of a specific asset.
        """
        account_data = self.get(
            endpoint=self.Endpoint.ACCOUNT,
            params={}
        )
        account_data = cast(Dict[str, Any], account_data)

        return [
            AssetBalance.loads(balance=balance)
            for balance in account_data[BinanceResponseKeys.BALANCES]
            if self._is_balance_non_zero(balance=balance)
        ]
    
    def get_balance(self) -> int:  # TODO: seems an extremely useless function.
        assets = self.get_portfolio()
        if assets is None:
            return 0
        return 2000
    
    def get_open_orders(self, symbol_id: str) -> List[Any]:
        """
        Retrieve current open orders
        """
        response = self.get(
            endpoint=self.Endpoint.OPEN_ORDERS,
            params={BinanceRequestKeys.SYMBOL: symbol_id}
        )
        return cast(List[Any], response)

    def get_orders(self, symbol_id: str, max_num_of_orders: int = 15) -> List[Any]:
        all_orders = self._get_all_orders(symbol_id=symbol_id)
        return all_orders[:max_num_of_orders]
    
    def get_recent_nav_snapshots(self, days: int = 2) -> List[AccountSnapshot]:  # replaces get_historical_nav in legace oms.Binance
        if days > 3:
            logger.warning(f"more than 3 days time window does not consider recent")
        history = []
        end_time = datetime.now(timezone.utc)

        for _ in range(days):
            snapshots = self._get_spot_account_snapshot(end_time=end_time)
            if not snapshots:
                break

            history = snapshots + history  # Prepend to maintain chronological order
            earliest_time = snapshots[0].update_time
            end_time = earliest_time - timedelta(hours=25)  # TODO: Not sure why 25 instead of 24, But I guess extra hour buffer to prevent overlap

        return history

    def get_deposits(self, params: dict) -> List[DepositRecord]:
        response_data = self.get(
            endpoint=self.Endpoint.DEPOSITS,
            params=params
        )
        response_data = cast(Dict[str, Any], response_data)

        deposits_data = response_data.get(BinanceResponseKeys.DEPOSITS_LIST)
        deposits_data = cast(List[Dict[str, Any]], deposits_data)
        return [
            DepositRecord.loads(deposit) for deposit in deposits_data
        ]
    
    def get_withdrawals(self, params: dict) -> List[WithdrawalRecord]:
        response_data = self.get(
            endpoint=self.Endpoint.WITHDRAWALS,
            params=params
        )
        response_data = cast(Dict[str, Any], response_data)

        withdrawals_list = response_data.get(BinanceResponseKeys.WITHDRAWAL_LIST)
        withdrawals_list = cast(List[Dict[str, Any]], withdrawals_list)
        return [
            WithdrawalRecord.loads(withdrawal) for withdrawal in withdrawals_list
        ]

    def get_transactions(self, params: dict) -> List[TransactionRecord]:
        deposits = self.get_deposits(params=params)
        withdrawals = self.get_withdrawals(params=params)
        transactions: List[TransactionRecord] = [
            TransactionRecord.loads(record=record)
            for record in deposits + withdrawals
        ]
        transactions = sorted(transactions, key=lambda x: x.time)
        return transactions


    def has_spot_trading_permission(self) -> bool:  # replaces verify in legacy oms.Binace
        response = self.get(endpoint=self.Endpoint.ACCOUNT)
        response = cast(Dict[str, Any], response)
        return (
            BinanceResponseKeys.PERMISSIONS in response and
            BinanceResponseValues.SPOT in response[BinanceResponseKeys.PERMISSIONS]
        )

    def _get_all_orders(self, symbol_id: str) -> List[Any]:
        """
        Retrieve historical orders for a symbol
        """
        response = self.get(
            endpoint=self.Endpoint.ALL_ORDERS,
            params={BinanceRequestKeys.SYMBOL: symbol_id}
        )
        orders = cast(List[Dict[str, Any]], response)
        return [
            order for order in reversed(orders)  # TODO: why are we reversing it?
            if self._is_order_meaningful(order=order)
        ]

    @staticmethod
    def _is_balance_non_zero(balance: Dict[str, Any]) -> bool:
        return (
            float(balance[BinanceResponseKeys.FREE]) > 0 or
            float(balance[BinanceResponseKeys.LOCKED]) > 0
        )
    
    @staticmethod
    def _is_order_meaningful(order: Dict[str, Any]) -> bool:
        return (
            float(order.get(BinanceResponseKeys.PRICE, 0)) > 0 or
            order.get(BinanceResponseKeys.TYPE) == OrderType.MARKET
        )

    def _get_spot_account_snapshot(  # replaces get_daily_snapshots in legacy oms.Binance
        self,
        limit: int = 30,   
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[AccountSnapshot]:
        response = self.get(
            endpoint=self.Endpoint.SNAPSHOT,
            params={
                BinanceRequestKeys.TYPE: BinanceRequestValues.SPOT,
                BinanceRequestKeys.LIMIT: limit,  # Number of snapshots to get
                BinanceRequestKeys.START_TIME: UnixMillis.from_dt_to_ms(start_time),
                BinanceRequestKeys.END_TIME: UnixMillis.from_dt_to_ms(end_time)
            }
        )
        response = cast(Dict[str, Any], response)
        snapshots = response.get(BinanceResponseKeys.SNAPSHOT_VOLUME_OBJECTS, [])
        return [AccountSnapshot.loads(snapshot=ss) for ss in snapshots]
