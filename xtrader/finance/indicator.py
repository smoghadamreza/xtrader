from typing import Any, Dict

import numpy as np
import pandas as pd
import talib
from talib import abstract

import data.redis as redis

columns = ["<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>", "<VOL>"]
fields = ["Open", "High", "Low", "Close", "Volume"]


class Indicator:
    def __init__(self, name=None, tail=None, interval=None):
        if not interval:
            raise Exception("interval is required")
        else:
            self.interval = interval
        if name:
            self.set_symbol(name, tail)
        else:
            self.name = ""
            self.df = pd.DataFrame()
            self.inputs = dict()

    def set_symbol(self, name, tail=None):
        self.symbold_id = name
        self.name = name
        self.df = self.load_db(tail)
        self.inputs = dict()
        for c in self.df.columns:
            if c != "time":
                self.inputs[c] = np.asarray(self.df[c], dtype="f8")

    def load_db(self, tail=None):
        db = redis.load_history(self.symbold_id, self.interval)
        if tail:
            for p in ["high", "low", "close", "open"]:
                db[p][-1] = tail["price"][p]
        df = pd.DataFrame(db)
        df.index = pd.Index(df["date"].values)
        df = df.loc[:, ["date", "open", "high", "low", "close", "volume"]]
        df.columns = ["time", "open", "high", "low", "close", "volume"]
        return df

    def ichimoku(self, *args, **kwargs):
        # conversion line period
        cl = float(kwargs["conversionLineperiod"])
        # base line
        bl = int(kwargs["BaseLineperiod"])
        # Sen span B
        ssB = float(kwargs["LagingB"])

        variable = {"function_name": "MAX", "price": "high", "timeperiod": cl}
        hh = pd.DataFrame(self.indicator_calculator(**variable))
        variable = {"function_name": "MIN", "price": "low", "timeperiod": cl}
        ll = pd.DataFrame(self.indicator_calculator(**variable))
        Tenkan = (ll + hh) / 2
        outdf = pd.DataFrame(Tenkan)

        variable = {"function_name": "MAX", "price": "high", "timeperiod": bl}
        hh = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        variable = {"function_name": "MIN", "price": "low", "timeperiod": bl}
        ll = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        kijun = (ll + hh) / 2

        senkouA = (Tenkan + kijun) / 2
        outdf["Kijun-sen"] = kijun
        outdf["Senkou Span A"] = senkouA.shift(bl)

        variable = {"function_name": "MAX", "price": "high", "timeperiod": ssB}
        hh = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        variable = {"function_name": "MIN", "price": "low", "timeperiod": ssB}
        ll = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        senkouB = (ll + hh) / 2
        outdf["Senkou Span B"] = senkouB.shift(bl)

        ls = pd.DataFrame(self.inputs["close"])
        ls.index = outdf.index
        ls = pd.DataFrame(ls.shift(-bl), copy=True)
        outdf["Chikou Span"] = ls
        outdf.columns = [
            "Tenkan-sen",
            "Kijun-sen",
            "Senkou Span A",
            "Senkou Span B",
            "Chikou Span",
        ]
        return outdf

    def indicator_calculator(
        self, function_name, symbol_name=None, tail=None, *args, **kwargs
    ):
        if symbol_name:
            self.set_symbol(symbol_name, tail)

        if function_name.lower() in self.df.columns:
            outdf = pd.DataFrame(self.df[function_name.lower()])
            outdf.columns = ["real"]
        elif function_name.lower() == "ichimoku":
            outdf = self.ichimoku(self.inputs, *args, **kwargs)
        elif function_name.lower() == "signal_line":
            c = 0
            if len(args) != 0:
                c = args[0]
            if kwargs:
                c = kwargs["value"]
            outdf = pd.DataFrame(
                c * np.ones([len(self.df), 1]),
                index=self.df.index,
                columns=["real"],
            )
        else:
            fun = abstract.Function(function_name.upper())
            output = fun(self.inputs, *args, **kwargs)
            # to handle multi Dimensional output
            outdf = pd.DataFrame()
            if isinstance(output[0], np.ndarray):
                for o in output:
                    outdf = pd.concat(
                        [outdf, pd.DataFrame(o, index=self.df.index)], axis=1
                    )
            else:
                outdf = pd.concat(
                    [outdf, pd.DataFrame(output, index=self.df.index)], axis=1
                )

            outdf.columns = fun.output_names
        return outdf


def get_parameter(function_name):
    fun = abstract.Function(function_name)
    md = dict()
    for t in list(fun.get_parameters().items()):
        md[t[0]] = t[1]
    return md


Rename_group_name_dic = {
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

Bad_indicators = ["MAVP"]


def get_group_api():
    # add signal lines to api
    mdic: Dict[Any, Any] = dict(
        signal_line=dict(
            fun_name="signal_line",
            params=dict(value=0),
            settings=dict(shift=0),
            outputs=dict(real=["line", "solid"]),
        )
    )
    # add ohlcv to api
    for field_name in fields:
        mdic[field_name] = dict(
            fun_name=field_name.lower(),
            settings=dict(shift=0),
            outputs=dict(real=["line", "solid"]),
        )
    mdic["Volume"]["outputs"]["real"][0] = "column"
    # add talib functions
    dic = dict()
    # keys are group names
    # value are indicators in a group
    for key, value in talib.get_function_groups().items():
        key = Rename_group_name_dic[key]
        if key:
            idic = dict()
            for fun_name in value:
                if fun_name not in Bad_indicators:
                    name = (
                        fun_name
                        + "("
                        + abstract.Function(fun_name).info["display_name"]
                        + ")"
                    )
                    idic[name] = dict(
                        fun_name=fun_name, settings=dict(shift=0)
                    )
                    idic[name]["params"] = get_parameter(fun_name)
                    output_dic = dict()
                    for li in list(
                        abstract.Function(fun_name).output_flags.items()
                    ):
                        output_dic[li[0]] = ["line", "solid"]
                        if li[1][0] == "Histogram":
                            output_dic[li[0]][0] = "column"
                        elif li[1][0] == "Dashed Line":
                            output_dic[li[0]][1] = "Dash"
                        elif li[1][0] == "star":
                            output_dic[li[0]][1] = "Dot"
                    idic[name]["outputs"] = output_dic
            dic[key] = idic
    dic["Historical Data"] = mdic
    return dic


def get_ti_api():
    dic: Dict[Any, Any] = dict(
        signal_line=dict(
            fun_name="signal_line",
            params=dict(value=0),
            settings=dict(shift=0),
            outputs=dict(real=["line", "solid"]),
        )
    )

    for field_name in fields:
        dic[field_name] = dict(
            fun_name=field_name.lower(),
            settings=dict(shift=0),
            outputs=dict(real=["line", "solid"]),
        )
    dic["Volume"]["outputs"]["real"][0] = "column"
    for fun_name in talib.get_functions():
        if fun_name not in Bad_indicators:
            name = (
                fun_name
                + "("
                + abstract.Function(fun_name).info["display_name"]
                + ")"
            )
            dic[name] = dict(fun_name=fun_name, settings=dict(shift=0))
            dic[name]["params"] = get_parameter(fun_name)
            output_dic = dict()
            for li in list(abstract.Function(fun_name).output_flags.items()):
                output_dic[li[0]] = ["line", "solid"]
                if li[1][0] == "Histogram":
                    output_dic[li[0]][0] = "column"
                elif li[1][0] == "Dashed Line":
                    output_dic[li[0]][1] = "Dash"
                elif li[1][0] == "star":
                    output_dic[li[0]][1] = "Dot"
            dic[name]["outputs"] = output_dic
    return dic


def add_time(df):
    outdf = pd.concat([pd.DataFrame(df.index, index=df.index), df], axis=1)
    outdf.columns = ["time"] + list(df.columns)
    return outdf


def to_json(df):
    return add_time(df).to_json(orient="values")


def read_json(json):
    df = pd.read_json(json)
    df = df.set_index(df[0]).iloc[:, 1:]
    return df
