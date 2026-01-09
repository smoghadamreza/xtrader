from typing import List
from .data import TradeRecord


class TradeHistoryManager:
    def __init__(self) -> None:
        self._records: List[TradeRecord] = []

    def add_trade(self, record: TradeRecord) -> None:
        self._records.append(record)

    def add_initial_buy(
        self,
        price: float,
        volume: int,
        realized_profit_loss: float,
        cash_balance: float,
        day_index: int,
    ) -> None:
        self.add_trade(
            TradeRecord(
                price=price,
                volume=volume,
                action="initial_buy",
                realized_profit_loss=realized_profit_loss,
                cash_balance=cash_balance,
                day_index=day_index,
            )
        )

    def add_rebuy(
        self,
        price: float,
        volume: int,
        realized_profit_loss: float,
        cash_balance: float,
        day_index: int,
    ) -> None:
        self.add_trade(
            TradeRecord(
                price=price,
                volume=volume,
                action="rebuy",
                realized_profit_loss=realized_profit_loss,
                cash_balance=cash_balance,
                day_index=day_index,
            )
        )

    def add_sell_exit(
        self,
        price: float,
        volume: int,
        realized_profit_loss: float,
        cash_balance: float,
        day_index: int,
    ) -> None:
        self.add_trade(
            TradeRecord(
                price=price,
                volume=volume,
                action="sell_exit",
                realized_profit_loss=realized_profit_loss,
                cash_balance=cash_balance,
                day_index=day_index,
            )
        )

    def get_records(self) -> List[TradeRecord]:
        return self._records
