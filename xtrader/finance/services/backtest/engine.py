from __future__ import annotations
from typing import List, Optional, Dict, Any, Union
import numpy as np
import pandas as pd
from utils.dataframe_utils import DataFrameUtils
from .data import Trade, Order, BackTestSummary, OrderAction


class BacktestEngine:
    """
    Engine to run backtests given price series, trade signals and configuration.
    
    Trades are stored as dataclasses internally. Output is serialized via to_dict().
    """

    def __init__(
        self,
        price: Union[pd.Series, pd.DataFrame],
        trades: Union[pd.Series, pd.DataFrame],
        config: Dict[str, Any],
    ):
        if isinstance(price, pd.DataFrame):
            price = DataFrameUtils.normalize_column_names(price).iloc[:, 0]
        if isinstance(trades, pd.DataFrame):
            trades = DataFrameUtils.normalize_column_names(trades).iloc[:, 0]

        self.price: pd.Series = DataFrameUtils.to_series(price).astype(float)
        self.trades: pd.Series = DataFrameUtils.to_series(trades).astype(int)
        self.config = config

        # Backtest parameters
        self.selling_commission = float(config.get("selling_commission", 0.01))
        self.buying_commission = float(config.get("buying_commission", 0.005))
        self.stop_loss_value = float(config.get("stop loss", 0))
        self.take_profit_value = float(config.get("take profit", 0))
        self.initial_capital = float(config.get("initial deposit", 100))

        # Optional apply series for stoploss/takeprofit triggers
        self.stop_loss_apply: Optional[pd.Series] = None
        self.take_profit_apply: Optional[pd.Series] = None
        if isinstance(config.get("stop loss"), dict) and config["stop loss"].get("apply") is not None:
            self.stop_loss_apply = DataFrameUtils.to_series(pd.Series(config["stop loss"]["apply"]))
        if isinstance(config.get("take profit"), dict) and config["take profit"].get("apply") is not None:
            self.take_profit_apply = DataFrameUtils.to_series(pd.Series(config["take profit"]["apply"]))

        # Runtime state
        self.trades_log: List[Trade] = []
        self.current_capital: float = self.initial_capital
        self.avg_returns: List[float] = []
        self.avg_days_in_trade: List[int] = []
        self.avg_days_waiting_for_new_trade: List[int] = []

    def run(self) -> Dict[str, Any]:
        position = 0
        asset = 0.0
        days_in_trade = 0
        days_waiting_for_new_trade = 0

        for i in range(len(self.trades)):
            signal = int(self.trades.iat[i])
            price = float(self.price.iat[i])

            # Open buy
            if position == 0 and signal == 1:
                asset = (1 + self.buying_commission) * price
                waiting = 0 if days_waiting_for_new_trade == 0 else i - days_waiting_for_new_trade
                buy_order = Order(
                    action=OrderAction.BUY,
                    date_index=str(i),
                    price=price,
                    waiting_candles=waiting
                )
                self.trades_log.append(Trade(buy=buy_order))
                position = 1
                days_in_trade = i

            # Close sell
            if position == 1 and signal == -1 and self.trades_log[-1].buy.date_index != str(i):
                profit_pct, candles = self._compute_profit(asset, price, days_in_trade)
                self._update_stats(profit_pct, candles)
                sell_order = Order(
                    action=OrderAction.SELL,
                    date_index=str(i),
                    price=price,
                    return_percent=profit_pct,
                    candles_in_trade=candles,
                    capital_after_trade=self.current_capital
                )
                self.trades_log[-1].sell = sell_order
                position = 0
                asset = 0.0
                days_in_trade = 0
                days_waiting_for_new_trade = i

            # Check takeprofit / stoploss
            if position == 1:
                # Take profit
                if self.take_profit_value != 0 and self.take_profit_apply is not None and i < len(self.take_profit_apply):
                    tp_price = float(self.take_profit_apply.iat[i])
                    tp_profit_pct = self._compute_profit_pct(asset, tp_price)
                    if tp_profit_pct > self.take_profit_value and self.trades_log[-1].buy.date_index != str(i):
                        profit_pct, candles = tp_profit_pct, i - days_in_trade + 1
                        self._update_stats(profit_pct, candles)
                        sell_order = Order(
                            action=OrderAction.TAKEPROFIT,
                            date_index=str(i),
                            price=tp_price,
                            return_percent=profit_pct,
                            candles_in_trade=candles,
                            capital_after_trade=self.current_capital
                        )
                        self.trades_log[-1].sell = sell_order
                        position = 0
                        asset = 0.0
                        days_in_trade = 0
                        days_waiting_for_new_trade = i

                # Stop loss
                if self.stop_loss_value != 0 and self.stop_loss_apply is not None and i < len(self.stop_loss_apply):
                    sl_price = float(self.stop_loss_apply.iat[i])
                    sl_profit_pct = self._compute_profit_pct(asset, sl_price)
                    if sl_profit_pct < -abs(self.stop_loss_value) and self.trades_log[-1].buy.date_index != str(i):
                        profit_pct, candles = sl_profit_pct, i - days_in_trade + 1
                        self._update_stats(profit_pct, candles)
                        sell_order = Order(
                            action=OrderAction.STOPLOSS,
                            date_index=str(i),
                            price=sl_price,
                            return_percent=profit_pct,
                            candles_in_trade=candles,
                            capital_after_trade=self.current_capital
                        )
                        self.trades_log[-1].sell = sell_order
                        position = 0
                        asset = 0.0
                        days_in_trade = 0
                        days_waiting_for_new_trade = i

        # Close last trade if still open
        if self.trades_log and not self.trades_log[-1].is_closed():
            i = len(self.trades) - 1
            final_price = float(self.price.iat[i])
            profit_pct, candles = self._compute_profit(asset, final_price, days_in_trade)
            self._update_stats(profit_pct, candles)
            sell_order = Order(
                action=OrderAction.NOT_SOLD_YET,
                date_index=str(i),
                price=final_price,
                return_percent=profit_pct,
                candles_in_trade=candles,
                capital_after_trade=self.current_capital
            )
            self.trades_log[-1].sell = sell_order

        # Build summary dataclass
        summary = BackTestSummary(
            avg_candles_in_trade=float(np.round(np.mean(self.avg_days_in_trade))) if self.avg_days_in_trade else 0,
            avg_waiting_candles=float(np.round(np.mean(self.avg_days_waiting_for_new_trade))) if self.avg_days_waiting_for_new_trade else 0,
            avg_return=float(np.round(np.mean(self.avg_returns) * 100) / 100) if self.avg_returns else 0,
            std_candles_in_trade=float(np.round(np.std(self.avg_days_in_trade))) if self.avg_days_in_trade else 0,
            std_waiting_candles=float(np.round(np.std(self.avg_days_waiting_for_new_trade))) if self.avg_days_waiting_for_new_trade else 0,
            std_return=float(np.round(np.std(self.avg_returns) * 100) / 100) if self.avg_returns else 0,
        )

        return {
            "trades": [t.to_dict() for t in self.trades_log],
            "summary": summary.to_dict()
        }

    def _compute_profit_pct(self, asset: float, price: float) -> float:
        return np.round(100 * (((1 - self.selling_commission) * price) - asset) / asset) / 100

    def _compute_profit(self, asset: float, price: float, days_in_trade: int) -> tuple[float, int]:
        profit_pct = self._compute_profit_pct(asset, price)
        candles = days_in_trade + 1
        return profit_pct, candles

    def _update_stats(self, profit_pct: float, candles: int):
        self.avg_returns.append(profit_pct)
        self.avg_days_in_trade.append(candles)
        self.current_capital = np.round(self.current_capital * ((100 + profit_pct) / 100))
