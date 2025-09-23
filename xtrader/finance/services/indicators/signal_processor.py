from __future__ import annotations
from typing import Union, Dict, Any

import numpy as np
import pandas as pd

from utils.dataframe_utils import DataFrameUtils


class SignalProcessor:
    """Encapsulates generation of trading signals from indicator data.

    Methods return pandas Series (single-column signals) to keep usage consistent.
    """

    @staticmethod
    def cross(shorter: Union[pd.Series, pd.DataFrame], longer: Union[pd.Series, pd.DataFrame]) -> pd.Series:
        """Return 1 for upward cross, -1 for downward cross, 0 otherwise.

        Works with Series or single-column DataFrames.
        """
        s = DataFrameUtils.to_series(shorter).astype(float)
        l = DataFrameUtils.to_series(longer).astype(float)
        prev_s = s.shift(1)
        prev_l = l.shift(1)

        up = (s > l) & (prev_s < prev_l)
        down = (s < l) & (prev_s > prev_l)
        out = np.zeros(len(s), dtype=int)
        out[up.fillna(False).to_numpy()] = 1
        out[down.fillna(False).to_numpy()] = -1
        return pd.Series(out, index=s.index)

    @staticmethod
    def cross_buy(shorter: Union[pd.Series, pd.DataFrame], longer: Union[pd.Series, pd.DataFrame]) -> pd.Series:
        s = DataFrameUtils.to_series(shorter).astype(float)
        l = DataFrameUtils.to_series(longer).astype(float)
        prev_s = s.shift(1)
        prev_l = l.shift(1)
        cond = (s > l) & (prev_s < prev_l)
        out = cond.fillna(False).astype(int)
        return pd.Series(out.values, index=s.index)

    @staticmethod
    def cross_sell(shorter: Union[pd.Series, pd.DataFrame], longer: Union[pd.Series, pd.DataFrame]) -> pd.Series:
        s = DataFrameUtils.to_series(shorter).astype(float)
        l = DataFrameUtils.to_series(longer).astype(float)
        prev_s = s.shift(1)
        prev_l = l.shift(1)
        cond = (s < l) & (prev_s > prev_l)
        out = cond.fillna(False).astype(int)
        return pd.Series(out.values, index=s.index)

    @staticmethod
    def merge(buy_signal: Union[pd.Series, pd.DataFrame], sell_signal: Union[pd.Series, pd.DataFrame]) -> pd.Series:
        buy = DataFrameUtils.to_series(buy_signal).astype(int)
        sell = DataFrameUtils.to_series(sell_signal).astype(int)
        out = np.zeros(len(buy), dtype=int)
        buy_idx = buy == 1
        sell_idx = sell == 1
        out[buy_idx.to_numpy()] = 1
        out[sell_idx.to_numpy()] = -1
        return pd.Series(out, index=buy.index)

    @staticmethod
    def monotono(indicator: Union[pd.Series, pd.DataFrame], days: int = 2) -> pd.Series:
        """Return 1 for ascending trend over `days`, -1 for descending, 0 otherwise."""
        s = DataFrameUtils.to_series(indicator).astype(float)
        diff = s.diff()
        asc = SignalProcessor._streak_positive(diff, days)
        desc = SignalProcessor._streak_negative(diff, days)
        out = np.zeros(len(s), dtype=int)
        out[asc.to_numpy()] = 1
        out[desc.to_numpy()] = -1
        return pd.Series(out, index=s.index)

    @staticmethod
    def _streak_positive(diff: pd.Series, days: int) -> pd.Series:
        """Helper: True where `diff` has been >0 for `days` periods (including current)."""
        n = len(diff)
        res = np.zeros(n, dtype=bool)
        arr = diff.fillna(0).to_numpy()
        for i in range(n):
            count = 0
            ok = True
            for j in range(days):
                idx = i - j
                if idx < 0:
                    ok = False
                    break
                if arr[idx] <= 0:
                    ok = False
                    break
            res[i] = ok
        return pd.Series(res, index=diff.index)

    @staticmethod
    def _streak_negative(diff: pd.Series, days: int) -> pd.Series:
        n = len(diff)
        res = np.zeros(n, dtype=bool)
        arr = diff.fillna(0).to_numpy()
        for i in range(n):
            ok = True
            for j in range(days):
                idx = i - j
                if idx < 0:
                    ok = False
                    break
                if arr[idx] >= 0:
                    ok = False
                    break
            res[i] = ok
        return pd.Series(res, index=diff.index)

    @staticmethod
    def more_than(main: Union[pd.Series, pd.DataFrame], minor: Union[pd.Series, pd.DataFrame], days: int = 0) -> pd.Series:
        main_s = DataFrameUtils.to_series(main).astype(float)
        minor_s = DataFrameUtils.to_series(minor).astype(float)
        diff = main_s - minor_s
        n = len(diff)
        res = np.zeros(n, dtype=int)
        arr = (diff >= 0).fillna(False).to_numpy()
        for i in range(n):
            ok = True
            for j in range(days + 1):
                idx = i - j
                if idx < 0:
                    ok = False
                    break
                if not arr[idx]:
                    ok = False
                    break
            if ok:
                res[i] = 1
        return pd.Series(res, index=diff.index)

    @staticmethod
    def special(indicators: Union[pd.DataFrame, Dict[str, Any]], name: str) -> pd.Series:
        """Dispatch special indicator logic (MACD, ichimoku, ...).

        Expected `indicators` is a dict-like mapping name->array/series OR a DataFrame.
        Returns a Series of signals (1/-1/0).
        """
        if name.lower() == "macd":
            return SignalProcessor._macd_signal(indicators)
        # placeholder for ichimoku or other special indicators
        if name.lower() == "ichimoku":
            # not implemented fully - return zeros
            idx = (
                indicators.index
                if isinstance(indicators, pd.DataFrame)
                else pd.Index(range(len(next(iter(indicators.values())))))
            )
            return pd.Series(np.zeros(len(idx), dtype=int), index=idx)
        raise NotImplementedError(f"Special indicator '{name}' not implemented")

    @staticmethod
    def _macd_signal(indicators: Union[pd.DataFrame, Dict[str, Any]]) -> pd.Series:
        """Compute MACD crosses using 'macd' and 'macdsignal' arrays in indicators."""
        if isinstance(indicators, pd.DataFrame):
            df = indicators
            macd = DataFrameUtils.to_series(df["macd"]) if "macd" in df else df.iloc[:, 0]
            macd_signal = DataFrameUtils.to_series(df["macdsignal"]) if "macdsignal" in df else df.iloc[:, 1]
        elif isinstance(indicators, dict):
            macd = pd.Series(indicators["macd"])
            macd_signal = pd.Series(indicators["macdsignal"])
        else:
            raise TypeError("indicators must be DataFrame or dict with 'macd' and 'macdsignal'")

        con1 = SignalProcessor.more_than(macd, macd_signal)
        con2 = SignalProcessor.more_than(macd_signal, macd)
        cross_sig = SignalProcessor.cross(macd, macd_signal)

        # multiply crosses by con1/con2 masks (only keep crosses if the condition holds)
        out = cross_sig.copy()
        out[(out == 1)] = out[(out == 1)] * con1[(out == 1)]
        out[(out == -1)] = out[(out == -1)] * con2[(out == -1)]
        return out.fillna(0).astype(int)
