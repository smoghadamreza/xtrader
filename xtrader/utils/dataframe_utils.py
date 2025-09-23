from __future__ import annotations
from typing import Union


import numpy as np
import pandas as pd

class DataFrameUtils:
    """
    Utility helpers for working with pandas DataFrames and Series used by the
    backtest/ signal code. These helpers are intentionally conservative and
    preserve indexes/columns for JSON compatibility.
    """

    @staticmethod
    def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Rename columns to string indices: '0', '1', ..."""
        df_copy = df.copy()
        df_copy.columns = [str(i) for i in range(df_copy.shape[1])]
        return df_copy

    @staticmethod
    def to_series(obj: Union[pd.DataFrame, pd.Series]) -> pd.Series:
        """Ensure input is a pandas Series. Convert single-column DataFrame to Series.

        Raises ValueError if a DataFrame with more than one column is provided.
        """
        if isinstance(obj, pd.Series):
            return obj
        if isinstance(obj, pd.DataFrame):
            if obj.shape[1] != 1:
                raise ValueError("DataFrame must have exactly one column to convert to Series")
            return obj.iloc[:, 0]
        raise TypeError("Input must be a pandas Series or single-column DataFrame")

    @staticmethod
    def shift(df: pd.DataFrame, periods: int) -> pd.DataFrame:
        """Shift DataFrame rows down by `periods` like pandas.DataFrame.shift."""
        return df.shift(periods).copy()

    @staticmethod
    def shift_with_fill(df: pd.DataFrame, periods: int, fill_value=np.nan) -> pd.DataFrame:
        """Shift DataFrame and fill the first `periods` rows with `fill_value`."""
        df_copy = df.copy()
        for i in range(min(periods, len(df_copy))):
            df_copy.iloc[i] = [fill_value] * df_copy.shape[1]
        return df_copy

    @staticmethod
    def propagate_last_valid(series: pd.Series, lookback: int = 0) -> pd.Series:
        """Replace zeros with the most recent non-zero value within `lookback`.

        Operates on a Series and returns a new Series with the same index.
        """
        s = series.copy()
        for i in range(len(s)):
            if s.iat[i] == 0:
                for j in range(1, min(lookback + 1, i + 1)):
                    if s.iat[i - j] != 0:
                        s.iat[i] = s.iat[i - j]
                        break
        return s
