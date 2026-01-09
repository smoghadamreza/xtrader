# backtest_service.py
from __future__ import annotations
import json
from typing import Any, Dict, Optional
import pandas as pd

from finance.services.indicators import Indicator
from .engine import BacktestEngine


class BacktestService:
    def __init__(self, indicator: Indicator):
        self.indicator = indicator

    def run_from_inputs(self, price_df: pd.DataFrame, trades_df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        price = pd.DataFrame(price_df).copy()
        trades_df = pd.DataFrame(trades_df).copy()

        for key in ["stop loss", "take profit"]:
            if key in config and isinstance(config[key], dict):
                apply_val = config[key].get("apply")
                if isinstance(apply_val, str):
                    series_df = self.indicator.calculate(apply_val)
                    if series_df.shape[1] > 1:
                        series_df = series_df.iloc[:, 0]
                    config[key]["apply"] = series_df

        engine = BacktestEngine(price, trades_df, config)
        return engine.run()

    def run(self, trades: Any, config: Dict[str, Any], get_json: bool = True) -> Any:
        price_df = self.indicator.calculate("close")
        for key in ["stop loss", "take profit"]:
            if key in config and isinstance(config[key], dict):
                apply_val = config[key].get("apply")
                if isinstance(apply_val, str):
                    series_df = self.indicator.calculate(apply_val)
                    if series_df.shape[1] > 1:
                        series_df = series_df.iloc[:, 0]
                    config[key]["apply"] = series_df

        trades_df = pd.DataFrame(trades)
        result = self.run_from_inputs(price_df, trades_df, config)

        if get_json:
            return json.dumps(result)
        return result
