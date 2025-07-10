import numpy as np
import pandas as pd


def cross(shorter, longer):
    shorter = change_df(shorter)
    longer = change_df(longer)
    output = np.where(
        (shorter > longer) & (shorter.shift(1) < longer.shift(1)),
        1,
        np.where(
            (shorter < longer) & (shorter.shift(1) > longer.shift(1)), -1, 0
        ),
    )
    return pd.DataFrame(output, index=shorter.index)


def cross_buy(shorter, longer):
    shorter = change_df(shorter)
    longer = change_df(longer)
    output = np.where(
        (shorter > longer) & (shorter.shift(1) < longer.shift(1)), 1, 0
    )
    return pd.DataFrame(output, index=shorter.index)


def cross_sell(shorter, longer):
    shorter = change_df(shorter)
    longer = change_df(longer)
    output = np.where(
        (shorter < longer) & (shorter.shift(1) > longer.shift(1)), 1, 0
    )
    return pd.DataFrame(output, index=shorter.index)


def merge(buy_df, sell_df):
    buy_df = change_df(buy_df)
    sell_df = change_df(sell_df)
    output = np.where((buy_df == 1), 1, np.where((sell_df == 1), -1, 0))
    return pd.DataFrame(output, index=buy_df.index)


def sell_output_for_display(df, signaldf):
    df = change_df(df)
    signaldf = change_df(signaldf)
    return df[signaldf == -1].dropna()


def buy_output_for_display(df, signaldf):
    df = change_df(df)
    signaldf = change_df(signaldf)
    return df[signaldf == 1].dropna()


def set_valid_time(df, time=0):
    outdf = pd.DataFrame(df, copy=True)
    for i in range(len(outdf)):
        if df.iloc[i, 0] == 0:
            for j in range(min(time, i)):
                if df.iloc[i - j - 1, 0] != 0:
                    outdf.at[df.index[i], outdf.columns[0]] = df.iloc[
                        i - j - 1, 0
                    ]
                    break
    return outdf


def shifter(df, shift_time):
    return pd.DataFrame(df.shift(shift_time), copy=True)


def shifter2(df, shift_time):
    for i in range(shift_time):
        df.iloc[0] = [np.nan for n in range(df.shape[1])]
    return df


def change_df(df):
    clmns = ""
    for i in range(df.shape[1]):
        clmns += str(i)
    clmns = list(clmns)
    mdf = pd.DataFrame(df, copy=True)
    mdf.columns = clmns

    return mdf


def monotono(indicator, days=2, angel=90):
    index = indicator.index
    current_day = change_df(indicator)
    result = pd.DataFrame(data=np.zeros(len(index)), index=index, columns=[0])
    previous_day = current_day.shift(1)
    mono = current_day.sub(previous_day, axis="index")
    result = ascending(mono, days, result)
    result = descending(mono, days, result)
    return result


def ascending(diff, days, result, value=100):
    index = diff.index
    mono = diff
    mono = mono > 0
    for i in range(len(index)):
        stat = mono["0"][index[i]]
        if stat:
            for j in range(days):
                stat = stat and mono["0"][index[i - j]]
        if stat:
            result[0][index[i]] = 1
    return result


def descending(diff, days, result):
    index = diff.index
    mono = diff
    mono = mono < 0
    for i in range(len(index)):
        stat = mono["0"][index[i]]
        if stat:
            for j in range(days):
                stat = stat and mono["0"][index[i - j]]
        if stat:
            result[0][index[i]] = -1
    return result


def more_than(main, minor, days=0):
    main = change_df(main)
    minor = change_df(minor)
    index = main.index
    result = pd.DataFrame(data=np.zeros(len(index)), index=index, columns=[0])
    diff = main.sub(minor, axis="index")
    mono = diff >= 0
    for i in range(len(index)):
        stat = mono["0"][index[i]]
        if bool(stat):
            for j in range(days):
                stat = stat and mono["0"][index[i - j]]
            result[0][index[i]] = 1
    return result


def special(indicators, name):
    if name == "MACD":
        return give_macd_result(indicators)
    elif name == "ichimoku":
        return give_ichimoku_result(indicators)


def give_ichimoku_result(indicators):
    indicators = pd.DataFrame(indicators, copy=True)


def give_macd_result(indicators):
    indicators = pd.DataFrame(indicators, copy=True)
    macd = pd.DataFrame(indicators["macd"])
    macdsignal = pd.DataFrame(indicators["macdsignal"])

    index = indicators.index
    result = pd.DataFrame(data=np.zeros(len(index)), index=index, columns=[0])

    con1 = more_than(macd, macdsignal)
    con2 = more_than(macdsignal, macd)
    result = cross(macd, result)

    for i in range(len(index)):
        if result[0][index[i]] == 1:
            result[0][index[i]] *= con1[0][index[i]]
        if result[0][index[i]] == -1:
            result[0][index[i]] *= con2[0][index[i]]

    return result


class BackTest:
    def __init__(self, price, trades, config):
        self.price = pd.DataFrame(change_df(price), copy=True)
        self.trades = pd.DataFrame(change_df(trades), copy=True)
        self.config = config
        self.stopLoss = float(config["stop loss"])
        self.takeProfit = float(config["take profit"])
        self.capital = int(config["initial deposit"])
        self.index = self.price.index
        self.trades.index = self.index
        self.result = {}
        self.trade = {}
        self.trade_num = 1
        self.avg_returns = []
        self.avg_days_in_tarde = []
        self.avg_days_waiting_for_new_trade = []
        self.position = 0
        self.asset = 0
        self.days_in_trade = 0
        self.days_waiting_for_new_trade = 0
        self.selling_commision = 0.01
        self.buying_commision = 0.005

    def order(self, details, kind):
        if kind == "sell":
            self.result[self.trade_num - 1][kind] = details

        elif kind == "buy":
            self.result[self.trade_num] = {}
            self.result[self.trade_num][kind] = details
            if self.trade_num == 1:
                self.result[self.trade_num]["buy"][
                    "initaial deposit"
                ] = self.capital
                self.result[self.trade_num]["buy"]["waiting candles"] = "Start"
        elif kind == "nothing":
            pass

    def change_other_things(self, kind, i):
        if kind == "sell":
            self.days_in_trade = 0
            self.position = 0
            self.asset = 0
        elif kind == "buy":
            self.days_waiting_for_new_trade = 0
            self.days_in_trade = i
            self.position = 1
            self.trade_num += 1

    def sell(self, i, sell_type):
        self.asset = (
            100
            * (
                ((1 - self.selling_commision) * self.price["0"][self.index[i]])
                - self.asset
            )
            / self.asset
        )
        self.asset = np.round(100 * self.asset) / 100
        self.avg_returns = self.avg_returns + [self.asset]
        self.days_in_trade = i - self.days_in_trade + 1
        self.avg_days_in_tarde = self.avg_days_in_tarde + [self.days_in_trade]
        self.days_waiting_for_new_trade = i
        self.capital = np.round(self.capital * ((100 + self.asset) / 100))
        return {
            "date": str(i),
            "action": sell_type,
            "price": str(self.price["0"][self.index[i]]),
            "return": str(self.asset),
            "candles in trade": self.days_in_trade,
            "capital": self.capital,
        }

    def buy(self, i):
        self.asset = (1 + self.buying_commision) * self.price["0"][
            self.index[i]
        ]
        if self.days_waiting_for_new_trade != 0:
            self.days_waiting_for_new_trade = (
                i - self.days_waiting_for_new_trade
            )
            self.avg_days_waiting_for_new_trade = (
                self.avg_days_waiting_for_new_trade
                + [self.days_waiting_for_new_trade]
            )
        return {
            "action": "buy",
            "date": str(i),
            "price": str(self.price["0"][self.index[i]]),
            "waiting candles": self.days_waiting_for_new_trade,
        }

    def check_last_trade(self):
        if len(self.result[self.trade_num - 1]) == 1:
            i = len(self.trades) - 1
            details = self.sell(i, "Not Sold Yet")
            self.order(details, "sell")
            self.change_other_things("sell", i)

    def summery(self):
        return {
            "average": {
                "candles in trade": np.round(np.mean(self.avg_days_in_tarde)),
                "waiting candles": np.round(
                    np.mean(self.avg_days_waiting_for_new_trade)
                ),
                "profits": np.round(np.mean(self.avg_returns) * 100) / 100,
            },
            "std": {
                "candles in trade": np.round(np.std(self.avg_days_in_tarde)),
                "waiting candles": np.round(
                    np.std(self.avg_days_waiting_for_new_trade)
                ),
                "profits": np.round(np.std(self.avg_returns) * 100) / 100,
            },
        }

    def call_order_and_change(self, details, order_type, i):
        self.order(details, order_type)
        self.change_other_things(order_type, i)

    def backtest_result(self):
        for i in range(len(self.trades)):
            order_type = "nothing"
            details = {}
            if self.position == 0 and self.trades["0"][self.index[i]] == 1:
                details = self.buy(i)
                order_type = "buy"
                self.call_order_and_change(details, order_type, i)
            elif (
                self.position == 1
                and self.trades["0"][self.index[i]] == -1
                and self.result[self.trade_num - 1]["buy"]["date"] != str(i)
            ):
                details = self.sell(i, "sell")
                order_type = "sell"
                self.call_order_and_change(details, order_type, i)
            if self.position == 1:
                if (
                    self.takeProfit != 0
                    and (
                        (1 - self.selling_commision)
                        * self.price["0"][self.index[i]]
                        - self.asset
                    )
                    > self.takeProfit
                    and self.result[self.trade_num - 1]["buy"]["date"]
                    != str(i)
                ):
                    details = self.sell(i, "takeprofit")
                    order_type = "sell"
                    self.call_order_and_change(details, order_type, i)
                if (
                    self.stopLoss != 0
                    and (
                        self.asset
                        - (1 - self.selling_commision)
                        * self.price["0"][self.index[i]]
                    )
                    > self.stopLoss
                ):
                    details = self.sell(i, "stoploss")
                    order_type = "sell"
                    self.call_order_and_change(details, order_type, i)
        self.check_last_trade()
        return self.result

    def back_test(self):
        result = self.backtest_result()
        summery = self.summery()
        return {"result": result, "summery": summery}


def testresult(price, trades, config):
    selling_commision = 0.001
    buying_commision = 0.001
    stopLoss = float(config["stop loss"]["value"])
    stopLossPrice = pd.DataFrame(
        change_df(config["stop loss"]["apply"]), copy=True
    )
    takeProfit = float(config["take profit"]["value"])
    takeProfitPrice = pd.DataFrame(
        change_df(config["take profit"]["apply"]), copy=True
    )
    capital = int(config["initial deposit"])
    price = pd.DataFrame(change_df(price), copy=True)
    trades = pd.DataFrame(change_df(trades), copy=True)
    index = price.index
    index = [str(i) for i in np.asarray(index)]
    takeProfitPrice.index = index
    stopLossPrice.index = index
    price.index = index
    trades.index = index
    result = {}

    trade_num = 1

    avg_returns = []
    avg_days_in_tarde = []
    avg_days_waiting_for_new_trade = []
    position = 0
    asset = 0
    days_in_trade = 0
    days_waiting_for_new_trade = 0

    for i in range(len(trades)):
        if position == 0 and trades["0"][index[i]] == 1:
            asset = (1 + buying_commision) * price["0"][index[i]]
            if days_waiting_for_new_trade != 0:
                days_waiting_for_new_trade = i - days_waiting_for_new_trade
                avg_days_waiting_for_new_trade = (
                    avg_days_waiting_for_new_trade
                    + [days_waiting_for_new_trade]
                )

            result[trade_num] = {}
            result[trade_num]["buy"] = {
                "action": "buy",
                "date": str(i),
                "price": str(price["0"][index[i]]),
                "waiting candles": days_waiting_for_new_trade,
            }
            if trade_num == 1:
                result[trade_num]["buy"]["initaial deposit"] = capital
                result[trade_num]["buy"]["waiting candles"] = "Start"

            days_waiting_for_new_trade = 0
            days_in_trade = i
            position = 1
            trade_num += 1
        if (
            position == 1
            and trades["0"][index[i]] == -1
            and result[trade_num - 1]["buy"]["date"] != str(i)
        ):
            asset = (
                100
                * (((1 - selling_commision) * price["0"][index[i]]) - asset)
                / asset
            )
            asset = np.round(100 * asset) / 100
            avg_returns = avg_returns + [asset]
            days_in_trade = i - days_in_trade + 1
            avg_days_in_tarde = avg_days_in_tarde + [days_in_trade]
            days_waiting_for_new_trade = i
            capital = np.round(capital * ((100 + asset) / 100))
            result[trade_num - 1]["sell"] = {
                "date": str(i),
                "action": "sell",
                "price": str(price["0"][index[i]]),
                "return": str(asset),
                "candles in trade": days_in_trade,
                "capital": capital,
            }

            days_in_trade = 0
            position = 0
            asset = 0
        if position == 1:
            if (
                takeProfit != 0
                and (
                    (1 - selling_commision) * takeProfitPrice["0"][index[i]]
                    - asset
                )
                > takeProfit
                and result[trade_num - 1]["buy"]["date"] != str(i)
            ):
                asset = (
                    100
                    * (
                        (
                            (1 - selling_commision)
                            * takeProfitPrice["0"][index[i]]
                        )
                        - asset
                    )
                    / asset
                )
                asset = np.round(100 * asset) / 100
                avg_returns = avg_returns + [asset]
                days_in_trade = i - days_in_trade + 1
                avg_days_in_tarde = avg_days_in_tarde + [days_in_trade]
                days_waiting_for_new_trade = i
                capital = np.round(capital * ((100 + asset) / 100))
                result[trade_num - 1]["sell"] = {
                    "date": str(i),
                    "action": "takeprofit",
                    "price": str(takeProfitPrice["0"][index[i]]),
                    "return": str(asset),
                    "candles in trade": days_in_trade,
                    "capital": capital,
                }
                days_in_trade = 0
                position = 0
                asset = 0
            if (
                stopLoss != 0
                and (
                    asset
                    - (1 - selling_commision) * stopLossPrice["0"][index[i]]
                )
                > stopLoss
                and result[trade_num - 1]["buy"]["date"] != str(i)
            ):
                asset = (
                    100
                    * (
                        (
                            (1 - selling_commision)
                            * stopLossPrice["0"][index[i]]
                        )
                        - asset
                    )
                    / asset
                )
                asset = np.round(100 * asset) / 100
                avg_returns = avg_returns + [asset]
                days_in_trade = i - days_in_trade + 1
                avg_days_in_tarde = avg_days_in_tarde + [days_in_trade]
                days_waiting_for_new_trade = i
                capital = np.round(capital * ((100 + asset) / 100))
                result[trade_num - 1]["sell"] = {
                    "date": str(i),
                    "action": "stoploss",
                    "price": str(stopLossPrice["0"][index[i]]),
                    "return": str(asset),
                    "candles in trade": days_in_trade,
                    "capital": capital,
                }

                days_in_trade = 0
                position = 0
                asset = 0
    if trade_num != 1 and len(result[trade_num - 1]) == 1:
        i = len(trades) - 1
        asset = 100 * ((0.99 * price["0"][index[i]]) - asset) / asset
        asset = np.round(100 * asset) / 100
        avg_returns = avg_returns + [asset]
        days_in_trade = i - days_in_trade + 1
        days_waiting_for_new_trade = i
        capital = np.round(capital * ((100 + asset) / 100))
        result[trade_num - 1]["sell"] = {
            "date": str(i),
            "action": "Not Sold Yet",
            "price": str(price["0"][index[i]]),
            "return": str(asset),
            "candles in trade": days_in_trade,
            "capital": capital,
        }
        days_in_trade = 0
        position = 0
        asset = 0

    backtest_result = {
        "result": result,
        "summery": {
            "average": {
                "candles in trade": (
                    np.round(np.mean(avg_days_in_tarde))
                    if len(avg_days_in_tarde) != 0
                    else 0
                ),
                "waiting candles": (
                    np.round(np.mean(avg_days_waiting_for_new_trade))
                    if len(avg_days_waiting_for_new_trade) != 0
                    else 0
                ),
                "profits": (
                    np.round(np.mean(avg_returns) * 100) / 100
                    if len(avg_returns) != 0
                    else 0
                ),
            },
            "std": {
                "candles in trade": (
                    np.round(np.std(avg_days_in_tarde))
                    if len(avg_days_in_tarde) != 0
                    else 0
                ),
                "waiting candles": (
                    np.round(np.std(avg_days_waiting_for_new_trade))
                    if len(avg_days_waiting_for_new_trade) != 0
                    else 0
                ),
                "profits": (
                    np.round(np.std(avg_returns) * 100) / 100
                    if len(avg_returns) != 0
                    else 0
                ),
            },
        },
    }
    if trade_num != 1:
        return backtest_result
    else:
        return "f"
