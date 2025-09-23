# indicators/indicator.py
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
from talib import abstract
from finance.services.exchange.binance import BinanceMarketService
from .indicator_data import IndicatorConfig


class Indicator:
    """
    Represents a technical indicator for a given symbol and timeframe.
    Handles data loading, preparation, and calculation.
    """

    def __init__(self, config: IndicatorConfig):
        if not config.interval:
            raise ValueError("Interval must be specified in IndicatorConfig.")

        self.config = config
        self.symbol = config.symbol
        self.interval = config.interval
        self.params = config.params

        self._market_service = BinanceMarketService()
        self.df: pd.DataFrame = self._load_candles()
        self.inputs: Dict[str, np.ndarray] = self._prepare_inputs()

    def _load_candles(self) -> pd.DataFrame:
        """Load OHLCV data for the symbol from Binance with caching."""
        candles = self._market_service.get_candles(
            symbol_id=self.symbol,
            interval=self.interval,
            use_redis_cache=True
        )
        df = pd.DataFrame([c.to_dict() for c in candles])
        df.index = pd.Index(df["open_time"].values)
        df = df[["open_time", "open_price", "high", "low", "close_price", "volume"]]
        df.columns = ["time", "open", "high", "low", "close", "volume"]
        return df

    def _prepare_inputs(self) -> Dict[str, np.ndarray]:
        """Convert dataframe columns to numpy arrays for TA-Lib calculations."""
        return {col: np.asarray(self.df[col], dtype="float64") for col in self.df.columns if col != "time"}

    def calculate(self, function_name: str, **kwargs) -> pd.DataFrame:
        """
        Calculate a technical indicator using TA-Lib abstract functions.
        Custom indicators like 'ichimoku' are handled separately.
        """
        function_name_lower = function_name.lower()

        if function_name_lower == "ichimoku":
            return self._ichimoku(**kwargs)

        # TA-Lib function
        try:
            func = abstract.Function(function_name.upper())
            output = func(self.inputs, **kwargs)
        except Exception as e:
            raise ValueError(f"Failed to calculate indicator '{function_name}': {e}")

        # Handle multi-output indicators
        if isinstance(output, tuple):
            df = pd.DataFrame({name: out for name, out in zip(func.output_names, output)}, index=self.df.index)
        else:
            df = pd.DataFrame(output, index=self.df.index, columns=func.output_names)

        return df

    def _ichimoku(self, conversion_line_period=9, base_line_period=26, lagging_span_b=52) -> pd.DataFrame:
        """
        Calculate Ichimoku Kinko Hyo indicator.
        Returns a DataFrame with Tenkan-sen, Kijun-sen, Senkou Span A/B, and Chikou Span.
        """
        high = self.inputs["high"]
        low = self.inputs["low"]
        close = self.inputs["close"]

        # Tenkan-sen (Conversion Line)
        tenkan = (pd.Series(high).rolling(conversion_line_period).max() +
                  pd.Series(low).rolling(conversion_line_period).min()) / 2

        # Kijun-sen (Base Line)
        kijun = (pd.Series(high).rolling(base_line_period).max() +
                 pd.Series(low).rolling(base_line_period).min()) / 2

        # Senkou Span A
        senkou_a = ((tenkan + kijun) / 2).shift(base_line_period)

        # Senkou Span B
        senkou_b = ((pd.Series(high).rolling(lagging_span_b).max() +
                     pd.Series(low).rolling(lagging_span_b).min()) / 2).shift(base_line_period)

        # Chikou Span
        chikou = pd.Series(close).shift(-base_line_period)

        return pd.DataFrame({
            "Tenkan-sen": tenkan,
            "Kijun-sen": kijun,
            "Senkou Span A": senkou_a,
            "Senkou Span B": senkou_b,
            "Chikou Span": chikou
        }, index=self.df.index)

    def to_json(self, df: Optional[pd.DataFrame] = None) -> str:
        """Convert a DataFrame to JSON including the timestamp."""
        df = df if df is not None else self.df
        df_with_time = df.copy()
        df_with_time["time"] = df_with_time.index
        return df_with_time.to_json(orient="records")
