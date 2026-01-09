from functools import cached_property
from typing import List, Dict, Any
import math

from finance.services.exchange.data import Candlestick
from finance.services.exchange.base import BaseExchangeMarketService
from finance.services.exchange.constants.binance import BinanceRequestValues
from .data import TradeRecord, MartingaleStrategyConfig
from .trade_history_manager import TradeHistoryManager


class MartingaleStopLossTakeProfitService:
    def __init__(
        self,
        market_service: BaseExchangeMarketService,
        config: MartingaleStrategyConfig,
    ):
        self._market_service = market_service
        self._config = config
        self._candlestick_history: List[Candlestick] = market_service.get_candles(
            symbol_id=config.symbol_id,
            interval=BinanceRequestValues.Interval.ONE_MINUTE,
        )
        self._trade_history_manager = TradeHistoryManager()

        self._sell_exit_triggered: bool = False
        self._total_volume: int = 0
        self._current_volume: int = 0
        self._current_day_index: int = 0
        self._cash_balance: float = 0.0  # equity balance after trades
        self._buy_indices: List[int] = []

    # --------------------
    # Public API
    # --------------------

    def run_strategy(self, start_index: int = 0) -> Dict[str, Any]:
        if start_index < 0 or start_index >= len(self._close_prices) - 1:
            raise IndexError("start_index out of range or too close to series end")

        initial_buy_price = self._handle_initial_buy(start_index=start_index)

        for current_idx in range(start_index + 1, len(self._close_prices)):
            self._current_day_index = current_idx
            rebuy_price = self._close_prices[current_idx]

            # NOTE: order of checks matters — Stop-Loss before Take-Profit here
            if rebuy_price < self.stop_loss_multiplier * initial_buy_price:
                self._handle_rebuy(rebuy_price=rebuy_price)
            elif self._high_prices[current_idx] >= (1.0 + self.take_profit_factor) * initial_buy_price:
                self._handle_take_profit()
                break

        result: Dict[str, Any] = {
            "history": [t.to_dict() for t in self._trade_history],
            "status": "completed" if self._sell_exit_triggered else "running",
            "buy_dates": [self._open_times[i] for i in self._buy_indices],
        }
        if self._sell_exit_triggered:
            result["finish_date"] = self._open_times[self._current_day_index]

        return result

    # --------------------
    # Trade simulation logic
    # --------------------

    def _handle_initial_buy(self, start_index: int) -> float:
        initial_buy_price = self._close_prices[start_index]
        self._current_day_index = start_index

        self._current_volume = 1
        self._total_volume = 1

        cost = self._current_volume * initial_buy_price
        self._cash_balance = self.initial_capital - cost

        self._trade_history_manager.add_initial_buy(
            price=initial_buy_price,
            volume=self._current_volume,
            realized_profit_loss=0.0,  # nothing realized yet
            cash_balance=self._cash_balance,
            day_index=start_index,
        )
        self._buy_indices.append(start_index)
        return initial_buy_price

    def _handle_rebuy(self, rebuy_price: float) -> None:
        rebuy_volume = self.calculate_rebuy_volume(rebuy_price=rebuy_price)
        cost = rebuy_volume * rebuy_price

        self._total_volume += rebuy_volume
        self._current_volume = rebuy_volume
        self._cash_balance -= cost

        self._trade_history_manager.add_rebuy(
            price=rebuy_price,
            volume=rebuy_volume,
            realized_profit_loss=0.0,  # still nothing realized
            cash_balance=self._cash_balance,
            day_index=self._current_day_index,
        )

        if self._cash_balance < 0:
            print("⚠️ margin call triggered")

        self._buy_indices.append(self._current_day_index)

    def _handle_take_profit(self) -> None:
        sell_price = self._high_prices[self._current_day_index]  # optimistic fill
        proceeds = sell_price * self._total_volume

        self._cash_balance += proceeds
        realized_profit_loss = self._cash_balance - self.initial_capital

        self._trade_history_manager.add_sell_exit(
            price=sell_price,
            volume=self._total_volume,
            realized_profit_loss=realized_profit_loss,
            cash_balance=self._cash_balance,
            day_index=self._current_day_index,
        )
        self._sell_exit_triggered = True

    # --------------------
    # Config accessors
    # --------------------

    @property
    def symbol_id(self) -> str:
        return self._config.symbol_id

    @property
    def stop_loss_multiplier(self) -> float:
        # e.g., config.stop_loss_factor = 0.05 -> multiplier = 0.95
        return 1.0 - self._config.stop_loss_factor

    @property
    def take_profit_factor(self) -> float:
        return self._config.take_profit_factor

    @property
    def initial_capital(self) -> float:
        return self._config.initial_capital

    # --------------------
    # Historical data helpers
    # --------------------

    @cached_property
    def _close_prices(self) -> List[float]:
        return [candle.close_price for candle in self._candlestick_history]

    @cached_property
    def _high_prices(self) -> List[float]:
        return [candle.high for candle in self._candlestick_history]

    @cached_property
    def _open_times(self) -> List[float]:
        return [candle.open_time for candle in self._candlestick_history]

    @property
    def _trade_history(self) -> List[TradeRecord]:
        return self._trade_history_manager.get_records()
    
    # --------------------
    # Core calculations
    # --------------------

    def calculate_rebuy_volume(self, rebuy_price: float) -> int:
        """
        Choose volume v so that at S = (1 + tp) * rebuy_price
        total profit_loss >= 0:  
        v * tp * rebuy_price >= sum_i max(0, vol_i * (price_i - S))
        """
        tp = self.take_profit_factor
        denom = tp * rebuy_price
        if denom <= 0:
            raise ValueError("take_profit_factor and rebuy_price must be > 0")

        numerator = sum(
            max(0.0, tr.volume * (tr.price - (1.0 + tp) * rebuy_price))
            for tr in self._trade_history
        )

        v = math.ceil(numerator / denom)
        return max(1, v)  # always rebuy at least 1 unit
