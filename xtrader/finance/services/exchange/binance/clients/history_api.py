from datetime import datetime, timedelta
from typing import cast, List, Dict, Any

from finance.models import Exchange

from .account_api import AccountAPIClient
from .authenticated_api import AuthenticatedAPIClient
from finance.services.exchange.constants.binance import BinanceRequestKeys
from finance.services.exchange.data import (
    DepositRecord, WithdrawalRecord, TradeRecord
)
from utils.unix_millis import UnixMillis


class HistoryAPIClient(AuthenticatedAPIClient):
    class Endpoint:
        MY_TRADES = AuthenticatedAPIClient.V3_ENDPOINT + "/myTrades"

    DEFAULT_HISTORY_DAYS = 2000
    WINDOW_DAYS_STEP = 89

    def __init__(self, user_exchange: Exchange, account_api_client: AccountAPIClient):
        super().__init__(user_exchange)
        self._account_api_client = account_api_client

    def get_historical_trades(self, symbol_id: str) -> List[TradeRecord]:
        from_id = 1
        trades = []
        while True:
            response_data = self.get(
                endpoint = self.Endpoint.MY_TRADES,
                params = {
                    BinanceRequestKeys.SYMBOL: symbol_id,
                    BinanceRequestKeys.FROM_ID: from_id,
                }
            )
            if not response_data:
                break
            trades_list_data = cast(List[Dict[str, Any]], response_data)
            trades = self._merge_unique_trades(
                list_a=trades,
                list_b=[
                    TradeRecord.loads(trade_data) 
                    for trade_data in trades_list_data
                ]
            )
            from_id = trades[-1].trade_id + 1
        return trades

    def get_historical_deposits(self) -> List[DepositRecord]:
        start_time = datetime.now() - timedelta(days=self.DEFAULT_HISTORY_DAYS)
        
        deposits = []
        while (current_time := start_time) <= datetime.now():
            end_time = current_time + timedelta(days=self.WINDOW_DAYS_STEP)
            deposits = self._merge_unique_deposits(
                list_a=deposits,
                list_b=self._account_api_client.get_deposits(
                    params={
                        BinanceRequestKeys.START_TIME: UnixMillis.from_dt_to_ms(current_time),
                        BinanceRequestKeys.END_TIME: UnixMillis.from_dt_to_ms(end_time)
                    }
                )
            )
            start_time = end_time
        return deposits

    def get_historical_withdrawals(self) -> List[WithdrawalRecord]:
        start_time = datetime.now() - timedelta(days=self.DEFAULT_HISTORY_DAYS)
        withdrawals = []

        while (current_time := start_time) <= datetime.now():
            end_time = current_time + timedelta(days=self.WINDOW_DAYS_STEP)
            withdrawals = self._merge_unique_withdrawals(
                list_a=withdrawals,
                list_b=self._account_api_client.get_withdrawals(
                    params={
                        BinanceRequestKeys.START_TIME: UnixMillis.from_dt_to_ms(current_time),
                        BinanceRequestKeys.END_TIME: UnixMillis.from_dt_to_ms(end_time)
                    }
                )
            )
            start_time = end_time
        return withdrawals

    @staticmethod
    def _merge_unique_trades(list_a: List[TradeRecord], list_b: List[TradeRecord]) -> List[TradeRecord]:
        """
        Merges two lists of TradeRecords, ensuring uniqueness based on trade_id.

        Args:
            list_a: First list of trades
            list_b: Second list of trades

        Returns:
            A merged list of unique TradeRecords, sorted by trade_id.
        """
        merged_dict = {trade.trade_id: trade for trade in list_a}
        for trade in list_b:
            merged_dict[trade.trade_id] = trade  # Overwrites if duplicate, or adds if new
        return sorted(merged_dict.values(), key=lambda t: t.trade_id)

    @staticmethod
    def _merge_unique_deposits(list_a: List[DepositRecord], list_b: List[DepositRecord]) -> List[DepositRecord]:
        """
        Merges two lists of DepositRecords, ensuring uniqueness based on transaction_id.

        Args:
            list_a: First list of deposits
            list_b: Second list of deposits

        Returns:
            A merged list of unique DepositRecords with respect to transaction_id.
        """
        merged_dict = {deposit.transaction_id: deposit for deposit in list_a}
        for deposit in list_b:
            merged_dict[deposit.transaction_id] = deposit  # Overwrites if duplicate, or adds if new
        return list(merged_dict.values())
    
    @staticmethod
    def _merge_unique_withdrawals(list_a: List[WithdrawalRecord], list_b: List[WithdrawalRecord]) -> List[WithdrawalRecord]:
        """
        Merges two lists of WithdrawalRecords, ensuring uniqueness based on withdrawal_id.

        Args:
            list_a: First list of withdrawals
            list_b: Second list of withdrawals

        Returns:
            A merged list of unique WithdrawalRecords with respect to withdrawal_id.
        """
        merged_dict = {withdrawal.withdrawal_id: withdrawal for withdrawal in list_a}
        for withdrawal in list_b:
            merged_dict[withdrawal.withdrawal_id] = withdrawal  # Overwrites if duplicate, or adds if new
        return list(merged_dict.values())
