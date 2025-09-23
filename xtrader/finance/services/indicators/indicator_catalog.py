from typing import Dict, Any
import talib
from talib import abstract

# Fields for basic OHLCV and custom signal line
FIELDS = ["Open", "High", "Low", "Close", "Volume"]
BAD_INDICATORS = ["MAVP"]

# Optional group renaming to match app UI
RENAME_GROUP_NAME = {
    "fields": "Historical Data",
    "Volume Indicators": "Volume Indicators",
    "Overlap Studies": "Trend Indicators",
    "Volatility Indicators": "Volatility Indicators",
    "Momentum Indicators": "Momentum Indicators",
    "Pattern Recognition": None,
    "Statistic Functions": None,
    "Price Transform": None,
    "Cycle Indicators": None,
    "Math Transform": None,
    "Math Operators": None,
}


def get_parameter(function_name: str) -> Dict[str, Any]:
    """Fetch default parameters for a TA-Lib function."""
    fun = abstract.Function(function_name)
    return dict(fun.get_parameters().items())


def get_group_api() -> Dict[str, Any]:
    """
    Build a full catalog of all available indicators and their metadata.
    Includes TA-Lib functions, OHLCV fields, and custom signal line.
    """
    # Historical data + signal line
    historical_data: Dict[str, Any] = {
        "signal_line": {
            "fun_name": "signal_line",
            "params": {"value": 0},
            "settings": {"shift": 0},
            "outputs": {"real": ["line", "solid"]},
        }
    }

    for field_name in FIELDS:
        historical_data[field_name] = {
            "fun_name": field_name.lower(),
            "settings": {"shift": 0},
            "outputs": {"real": ["line", "solid"]},
        }
    historical_data["Volume"]["outputs"]["real"][0] = "column"

    catalog: Dict[str, Any] = {"Historical Data": historical_data}

    # TA-Lib indicator groups
    for group_name, functions in talib.get_function_groups().items():
        mapped_group = RENAME_GROUP_NAME.get(group_name)
        if not mapped_group:
            continue

        group_dict: Dict[str, Any] = {}
        for func_name in functions:
            if func_name in BAD_INDICATORS:
                continue
            display_name = abstract.Function(func_name).info.get("display_name", func_name)
            key = f"{func_name} ({display_name})"

            output_flags = abstract.Function(func_name).output_flags
            outputs = {}
            for out_name, flag in output_flags.items():
                out_type = "line"
                style = "solid"
                if flag[0] == "Histogram":
                    out_type = "column"
                elif flag[0] == "Dashed Line":
                    style = "Dash"
                elif flag[0] == "star":
                    style = "Dot"
                outputs[out_name] = [out_type, style]

            group_dict[key] = {
                "fun_name": func_name,
                "params": get_parameter(func_name),
                "settings": {"shift": 0},
                "outputs": outputs,
            }
        catalog[mapped_group] = group_dict

    return catalog
