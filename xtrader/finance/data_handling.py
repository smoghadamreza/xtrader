import json
from typing import Dict, Any

import numpy as np
import pandas as pd

from finance import backtest as bt
from finance import indicator
from finance.indicator import Indicator


def give_result_more(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    valid = int(data["valid"])
    indicators: Dict[str, Any] = {"main": {}, "minor": {}}

    main = {"function_name": data["indicators"]["main"]["name"]}
    main = add_apply_to(main, "main", data)
    if "params" in data["indicators"]["main"]:
        params = data["indicators"]["main"]["params"]
        for param in params:
            main[param] = float(params[param])
            if int(main[param]) == main[param]:
                main[param] = int(main[param])

    indicator_main_org = bt.shifter(
        mt.indicator_calculator(**main),
        int(data["indicators"]["main"]["settings"]["shift"]),
    )
    indicator_main = indicator_main_org[
        data["indicators"]["main"]["output"]["name"]
    ]
    indicator_main = pd.DataFrame(indicator_main)

    outputs = data["indicators"]["main"]["outputs"]
    for output in outputs:
        indicators["main"][output] = indicator.add_time(
            pd.DataFrame(indicator_main_org[output])
        ).to_json(orient="values")

    minor = {"function_name": data["indicators"]["minor"]["name"]}
    minor = add_apply_to(minor, "minor", data)
    if "params" in data["indicators"]["minor"]:
        params = data["indicators"]["minor"]["params"]
        for param in params:
            minor[param] = float(params[param])
            if int(minor[param]) == minor[param]:
                minor[param] = int(minor[param])

    indicator_minor_org = bt.shifter(
        mt.indicator_calculator(**minor),
        int(data["indicators"]["minor"]["settings"]["shift"]),
    )
    indicator_minor = indicator_minor_org[
        data["indicators"]["minor"]["output"]["name"]
    ]
    indicator_minor = pd.DataFrame(indicator_minor)

    outputs = data["indicators"]["minor"]["outputs"]
    for output in outputs:
        indicators["minor"][output] = indicator.add_time(
            pd.DataFrame(indicator_minor_org[output])
        ).to_json(orient="values")

    more = bt.more_than(indicator_main, indicator_minor)
    more = bt.set_valid_time(bt.change_df(more), valid)

    indicators["type"] = "second"
    indicators["result"] = more.to_json(orient="values")
    if not get_json:
        return indicators
    return json.dumps(indicators)


def give_result_special(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    valid = int(data["valid"])
    special = {"function_name": data["indicators"]["special"]["name"]}
    special = add_apply_to(special, "special", data)
    if "params" in data["indicators"]["special"]:
        params = data["indicators"]["special"]["params"]
        for param in params:
            special[param] = float(params[param])
            if int(special[param]) == special[param]:
                special[param] = int(special[param])

    indicator_special_org = bt.shifter(
        mt.indicator_calculator(**special),
        int(data["indicators"]["special"]["settings"]["shift"]),
    )

    outputs = data["indicators"]["special"]["outputs"]
    indicators: Dict[str, Any] = {"special": {}}
    for output in outputs:
        indicators["special"][output] = indicator.add_time(
            pd.DataFrame(indicator_special_org[output])
        ).to_json(orient="values")

    result = bt.special(
        indicator_special_org, data["indicators"]["special"]["name"]
    )
    result = bt.set_valid_time(result, valid)

    indicators["result"] = result.to_json(orient="values")
    indicators["type"] = "first"
    if not get_json:
        return indicators
    return json.dumps(indicators)


def give_result_ascending(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    days = int(data["days"])
    valid = int(data["valid"])
    ascending = {"function_name": data["indicators"]["ascending"]["name"]}
    ascending = add_apply_to(ascending, "ascending", data)
    if "params" in data["indicators"]["ascending"]:
        params = data["indicators"]["ascending"]["params"]
        for param in params:
            ascending[param] = float(params[param])
            if ascending[param] == int(ascending[param]):
                ascending[param] = int(ascending[param])

    indicator_ascending_org = bt.shifter(
        mt.indicator_calculator(**ascending),
        int(data["indicators"]["ascending"]["settings"]["shift"]),
    )
    indicator_ascending = indicator_ascending_org[
        data["indicators"]["ascending"]["output"]["name"]
    ]
    indicator_ascending = pd.DataFrame(indicator_ascending)

    outputs = data["indicators"]["ascending"]["outputs"]
    indicators: Dict[str, Any] = {"ascending": {}}
    for output in outputs:
        indicators["ascending"][output] = indicator.add_time(
            pd.DataFrame(indicator_ascending_org[output])
        ).to_json(orient="values")
    result = bt.monotono(indicator_ascending, days)
    result = bt.set_valid_time(result, valid)
    indicators["type"] = "first"
    indicators["result"] = result.to_json(orient="values")
    if not get_json:
        return indicators
    return json.dumps(indicators)


def give_result_draw(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    draw = {"function_name": data["indicators"]["draw"]["name"]}
    draw = add_apply_to(draw, "draw", data)
    if "params" in data["indicators"]["draw"]:
        params = data["indicators"]["draw"]["params"]
        for param in params:
            draw[param] = float(params[param])
            if int(draw[param]) == draw[param]:
                draw[param] = int(draw[param])

    indicator_draw_org = bt.shifter(
        mt.indicator_calculator(**draw),
        int(data["indicators"]["draw"]["settings"]["shift"]),
    )
    outputs = data["indicators"]["draw"]["outputs"]
    indicators: Dict[str, Any] = {"draw": {}}
    for output in outputs:
        indicators["draw"][output] = indicator.add_time(
            pd.DataFrame(indicator_draw_org[output])
        ).to_json(orient="values")

    indicators["type"] = "default"

    if not get_json:
        return indicators
    return json.dumps(indicators)


def give_result_candlestick(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    valid = int(data["valid"])
    candlestick = {"function_name": data["indicators"]["candlestick"]["name"]}
    if "params" in data["indicators"]["candlestick"]:
        params = data["indicators"]["candlestick"]["params"]
        for param in params:
            candlestick[param] = float(params[param])

    indicator_candlestick_org = bt.shifter(
        mt.indicator_calculator(**candlestick),
        int(data["indicators"]["candlestick"]["settings"]["shift"]),
    )
    indicator_candlestick = indicator_candlestick_org[
        data["indicators"]["candlestick"]["output"]["name"]
    ]
    indicator_candlestick = pd.DataFrame(indicator_candlestick)

    indicators: Dict[str, Any] = {"candlestick": {}}
    outputs = data["indicators"]["candlestick"]["outputs"]
    for output in outputs:
        indicators["candlestick"][output] = indicator.add_time(
            pd.DataFrame(indicator_candlestick_org[output])
        ).to_json(orient="values")

    indicator_candlestick = indicator_candlestick.replace([100, -100], [1, -1])
    result = indicator_candlestick

    result = bt.set_valid_time(result, valid)

    indicators["type"] = "first"
    indicators["result"] = result.to_json(orient="values")
    if not get_json:
        return indicators
    return json.dumps(indicators)


def give_result_cross(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    valid = int(data["valid"])
    indicators: Dict[str, Any] = {"shorter": {}, "longer": {}}

    shorter = {"function_name": data["indicators"]["shorter"]["name"]}
    shorter = add_apply_to(shorter, "shorter", data)
    if "params" in data["indicators"]["shorter"]:
        params = data["indicators"]["shorter"]["params"]
        for param in params:
            shorter[param] = float(params[param])
            if shorter[param] == int(shorter[param]):
                shorter[param] = int(shorter[param])

    indicator_shorter_org = bt.shifter(
        mt.indicator_calculator(**shorter),
        int(data["indicators"]["shorter"]["settings"]["shift"]),
    )
    indicator_shorter = indicator_shorter_org[
        data["indicators"]["shorter"]["output"]["name"]
    ]
    indicator_shorter = pd.DataFrame(indicator_shorter)

    outputs = data["indicators"]["shorter"]["outputs"]
    for output in outputs:
        indicators["shorter"][output] = indicator.add_time(
            pd.DataFrame(indicator_shorter_org[output])
        ).to_json(orient="values")

    longer = {"function_name": data["indicators"]["longer"]["name"]}
    longer = add_apply_to(longer, "longer", data)
    if "params" in data["indicators"]["longer"]:
        params = data["indicators"]["longer"]["params"]
        for param in params:
            longer[param] = float(params[param])
            if longer[param] == int(longer[param]):
                longer[param] = int(longer[param])

    indicator_longer_org = bt.shifter(
        mt.indicator_calculator(**longer),
        int(data["indicators"]["longer"]["settings"]["shift"]),
    )
    indicator_longer = indicator_longer_org[
        data["indicators"]["longer"]["output"]["name"]
    ]
    indicator_longer = pd.DataFrame(indicator_longer)
    outputs = data["indicators"]["longer"]["outputs"]
    for output in outputs:
        indicators["longer"][output] = indicator.add_time(
            pd.DataFrame(indicator_longer_org[output])
        ).to_json(orient="values")

    cross = bt.cross(indicator_shorter, indicator_longer)
    cross = bt.set_valid_time(cross, valid)

    indicators["type"] = "first"
    indicators["result"] = cross.to_json(orient="values")
    if not get_json:
        return indicators
    return json.dumps(indicators)


def give_result_advance_cross(data, mt=None, get_json=True, interval=None):
    if mt is None:
        mt = Indicator(name=data["symbol_id"], interval=interval)
    valid = int(data["valid"])
    indicators: Dict[str, Any] = {
        "buying shorter": {},
        "buying longer": {},
        "selling shorter": {},
        "selling longer": {},
    }

    selling_shorter = {
        "function_name": data["indicators"]["selling shorter"]["name"]
    }
    selling_shorter = add_apply_to(selling_shorter, "selling shorter", data)
    if "params" in data["indicators"]["selling shorter"]:
        params = data["indicators"]["selling shorter"]["params"]
        for param in params:
            selling_shorter[param] = float(params[param])
            if int(selling_shorter[param]) == selling_shorter[param]:
                selling_shorter[param] = int(selling_shorter[param])

    indicator_selling_shorter_org = bt.shifter(
        mt.indicator_calculator(**selling_shorter),
        int(data["indicators"]["selling shorter"]["settings"]["shift"]),
    )
    indicator_selling_shorter = indicator_selling_shorter_org[
        data["indicators"]["selling shorter"]["output"]["name"]
    ]
    indicator_selling_shorter = pd.DataFrame(indicator_selling_shorter)

    outputs = data["indicators"]["selling shorter"]["outputs"]
    for output in outputs:
        indicators["selling shorter"][output] = indicator.add_time(
            pd.DataFrame(indicator_selling_shorter_org[output])
        ).to_json(orient="values")

    selling_longer = {
        "function_name": data["indicators"]["selling longer"]["name"]
    }
    selling_longer = add_apply_to(selling_longer, "selling longer", data)
    if "params" in data["indicators"]["selling longer"]:
        params = data["indicators"]["selling longer"]["params"]
        for param in params:
            selling_longer[param] = float(params[param])
            if int(selling_longer[param]) == selling_longer[param]:
                selling_longer[param] = int(selling_longer[param])

    indicator_selling_longer_org = bt.shifter(
        mt.indicator_calculator(**selling_longer),
        int(data["indicators"]["selling longer"]["settings"]["shift"]),
    )
    indicator_selling_longer = indicator_selling_longer_org[
        data["indicators"]["selling longer"]["output"]["name"]
    ]
    indicator_selling_longer = pd.DataFrame(indicator_selling_longer)
    outputs = data["indicators"]["selling longer"]["outputs"]
    for output in outputs:
        indicators["selling longer"][output] = indicator.add_time(
            pd.DataFrame(indicator_selling_longer_org[output])
        ).to_json(orient="values")

    selling_cross = bt.cross(
        indicator_selling_shorter, indicator_selling_longer
    ).replace([1], [0])

    buying_shorter = {
        "function_name": data["indicators"]["buying shorter"]["name"]
    }
    buying_shorter = add_apply_to(buying_shorter, "buying shorter", data)
    if "params" in data["indicators"]["buying shorter"]:
        params = data["indicators"]["buying shorter"]["params"]
        for param in params:
            buying_shorter[param] = float(params[param])
            if int(buying_shorter[param]) == buying_shorter[param]:
                buying_shorter[param] = int(buying_shorter[param])

    indicator_buying_shorter_org = bt.shifter(
        mt.indicator_calculator(**buying_shorter),
        int(data["indicators"]["buying shorter"]["settings"]["shift"]),
    )
    indicator_buying_shorter = indicator_buying_shorter_org[
        data["indicators"]["buying shorter"]["output"]["name"]
    ]
    indicator_buying_shorter = pd.DataFrame(indicator_buying_shorter)

    outputs = data["indicators"]["buying shorter"]["outputs"]
    for output in outputs:
        indicators["buying shorter"][output] = indicator.add_time(
            pd.DataFrame(indicator_buying_shorter_org[output])
        ).to_json(orient="values")

    buying_longer = {
        "function_name": data["indicators"]["buying longer"]["name"]
    }
    buying_longer = add_apply_to(buying_longer, "buying longer", data)
    if "params" in data["indicators"]["buying longer"]:
        params = data["indicators"]["buying longer"]["params"]
        for param in params:
            buying_longer[param] = float(params[param])
            if int(buying_longer[param]) == buying_longer[param]:
                buying_longer[param] = int(buying_longer[param])

    indicator_buying_longer_org = bt.shifter(
        mt.indicator_calculator(**buying_longer),
        int(data["indicators"]["buying longer"]["settings"]["shift"]),
    )
    indicator_buying_longer = indicator_buying_longer_org[
        data["indicators"]["buying longer"]["output"]["name"]
    ]
    indicator_buying_longer = pd.DataFrame(indicator_buying_longer)
    outputs = data["indicators"]["buying longer"]["outputs"]
    for output in outputs:
        indicators["buying longer"][output] = indicator.add_time(
            pd.DataFrame(indicator_buying_longer_org[output])
        ).to_json(orient="values")

    buying_cross = bt.cross(
        indicator_buying_shorter, indicator_buying_longer
    ).replace([-1], [0])
    cross = buying_cross + selling_cross
    cross = bt.set_valid_time(cross, valid)

    indicators["type"] = "first"
    indicators["result"] = cross.to_json(orient="values")
    if not get_json:
        return indicators
    return json.dumps(indicators)


def add_to_db(id, data):
    pass


def give_result_backtest(name, res, config, interval=None):
    mt = Indicator(name=name, interval=interval)
    price = {"function_name": "close"}
    price = mt.indicator_calculator(**price)
    for setting in ["stop loss", "take profit"]:
        config[setting]["apply"] = mt.indicator_calculator(
            **{"function_name": config[setting]["apply"]}
        )
    res = pd.DataFrame(data=res)
    result = bt.testresult(price, res, config)
    return json.dumps(result)


def give_update_indicators(data):
    price = data["price"]
    data = data["params"]
    draw = {"function_name": data["name"]}
    draw = add_apply_to(draw, "draw", data)
    length = 5
    if "params" in data:
        params = data["params"]
        for param in params:
            draw[param] = float(params[param])
            length = np.max([length, np.abs(float(params[param]))])
    length = 10 * (int(length) + 2)
    tail = {"price": price, "length": length}
    mt = Indicator(name=data["symbol_id"], tail=tail)
    indicator_draw_org = mt.indicator_calculator(**draw)
    outputs = data["outputs"]
    indicators = {}
    for output in outputs:
        indicators[outputs[output]["id"]] = indicator.add_time(
            pd.DataFrame(indicator_draw_org[output].tail(1))
        ).to_json(orient="values")
    return json.dumps(indicators)


def add_apply_to(indicator_dic, indicator_name, data):
    if data["indicators"][indicator_name]["apply_to"] != "default":
        indicator_dic["price"] = data["indicators"][indicator_name]["apply_to"]
    return indicator_dic
