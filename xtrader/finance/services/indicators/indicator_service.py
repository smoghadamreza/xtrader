import json
from typing import Any, Dict
import pandas as pd

from finance.services.backtest import backtest_service as bt_service
from finance.services.indicators.signal_processor import SignalProcessor
from utils.consts import XtraderRequestKeys
from finance.exceptions import RequiredKeyMissing, InvalidIndicatorType
from .indicator import Indicator
from .indicator_data import IndicatorConfig, IndicatorTypes


class IndicatorService:
    """
    Service class to calculate indicators and run backtests.
    Encapsulates Indicator and BacktestService usage.
    """

    def __init__(self, symbol: str, interval: str):
        self.symbol = symbol
        self.interval = interval
        self.indicator = Indicator(IndicatorConfig(symbol=symbol, interval=interval, params={}))
        self.backtest_service = bt_service.BacktestService(self.indicator)

    def calculate(
        self, data: Dict[str, Any], indicator_type: str
    ) -> Dict[str, Any]:
        """
        Calculate any indicator type: main, minor, special, ascending, draw, etc.
        """
        ind_data = data["indicators"][indicator_type]
        valid = int(data.get("valid", 0))

        # Prepare parameters
        params = {}
        for k, v in ind_data.get("params", {}).items():
            v = float(v)
            if int(v) == v:
                v = int(v)
            params[k] = v

        # Determine price column
        if ind_data.get("apply_to") and ind_data["apply_to"] != "default":
            params["price"] = ind_data["apply_to"]

        # Calculate indicator
        df_org = self.indicator.calculate(ind_data["name"], **params)

        # Apply shift if any
        shift = int(ind_data.get("settings", {}).get("shift", 0))
        if shift != 0:
            df_org = df_org.shift(shift)

        # Prepare outputs
        outputs = ind_data.get("outputs", [])
        indicators: Dict[str, Any] = {indicator_type: {}}
        for output in outputs:
            if output in df_org:
                indicators[indicator_type][output] = self._add_time_to_json(df_org[output])

        # Special result handling using SignalProcessor
        if indicator_type in ["main", "minor"]:
            more = SignalProcessor.more_than(pd.DataFrame(df_org), pd.DataFrame(df_org))
            more = more.iloc[valid:]
            indicators["type"] = "second"
            indicators["result"] = more.to_json(orient="values")
        elif indicator_type == "ascending":
            days = int(data.get("days", 1))
            result = SignalProcessor.monotono(pd.DataFrame(df_org), days).iloc[valid:]
            indicators["type"] = "first"
            indicators["result"] = result.to_json(orient="values")
        elif indicator_type == "special":
            result = SignalProcessor.special(df_org, ind_data["name"]).iloc[valid:]
            indicators["type"] = "first"
            indicators["result"] = result.to_json(orient="values")
        elif indicator_type == "candlestick":
            df_org = df_org.replace([100, -100], [1, -1])
            result = df_org.iloc[valid:]
            indicators["type"] = "first"
            indicators["result"] = result.to_json(orient="values")
        elif indicator_type in ["cross", "advance_cross"]:
            cross_result = pd.DataFrame(df_org).iloc[valid:]
            indicators["type"] = "first"
            indicators["result"] = cross_result.to_json(orient="values")
        else:
            indicators["type"] = "default"
            indicators["result"] = df_org.iloc[valid:].to_json(orient="values")

        return indicators

    def _add_time_to_json(self, series: pd.Series) -> str:
        """Add time index to a series or dataframe and convert to JSON."""
        df_copy = pd.DataFrame(series)
        df_copy["time"] = df_copy.index
        return df_copy.to_json(orient="values")
    
    def  caculate_indicators(self, request_data: Dict[str, Any]):
        try:
            indicator_type: str = request_data[XtraderRequestKeys.INDICATOR_TYPE]
            indicator_type = indicator_type.lower()

            if not IndicatorTypes.is_valid(indicator_type=indicator_type):
                raise InvalidIndicatorType(indicator_type=indicator_type)
            return self.give_result(
                data=request_data,
                kind=indicator_type,
            )
        except KeyError:
            raise RequiredKeyMissing()
            

    def give_result(self, data: Dict[str, Any], kind: str, get_json: bool = True):
        """Calculate any indicator kind and return JSON or dict."""
        result = self.calculate(data, kind)
        return json.dumps(result) if get_json else result

    def give_result_backtest(
        self, res: Any, config: Dict[str, Any], get_json: bool = True
    ):
        """
        Run backtest using BacktestService.
        Automatically handles price and indicator-based stop loss / take profit.
        """
        return self.backtest_service.run(
            trades=res,
            config=config,
            get_json=get_json
        )
