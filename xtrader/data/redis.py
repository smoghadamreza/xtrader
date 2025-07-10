import json
import time
from typing import List, cast

import redis
import requests
from django.conf import settings

r = redis.Redis(host="redis", port=6379, db=settings.REDIS_DB)
needed_keys = ["date", "open", "high", "low", "close", "volume"]
intervals = settings.INTERVALS


def hgetall(name):
    result = cast(List[bytes], r.hgetall(name))
    if result:
        return [res.decode() for res in result]
    return []


def set(name, value):
    return r.set(name=name, value=value)


def get(name):
    return cast(bytes, r.get(name=name)).decode()


def hset(name, key, value):
    return r.hset(name=name, key=key, value=value)


def hget(name, key):
    value = cast(bytes, r.hget(name=name, key=key))
    if value is None:
        return {}

    return json.loads(value.decode())


def delete(names):
    return r.delete(*names)


def keys():
    return r.keys()


def set_history(name, interval):
    history_name = get_history_name(name, interval)
    params = {
        "symbol": name,
        "interval": interval,
        "limit": settings.CANDLES_HISTORY_LIMIT,
    }
    print("getting:", history_name)
    data = requests.get(
        "https://api.binance.com/api/v3/klines", params=params
    ).json()
    print(data)
    data_dict = {
        "date": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
        "volume": [],
    }
    for d in data[:-1]:
        for i, k in enumerate(needed_keys):
            value = d[i]
            if isinstance(value, str):
                data_dict[k].append(float(value))
            else:
                data_dict[k].append(value)
    for key, value in data_dict.items():
        hset(history_name, key, value)


def get_history_name(name, interval):
    return "{}-{}".format(name.upper(), interval)


def load_history(name, interval, num=0):
    if num > 1:
        return {}
    name = name.upper()
    history_name = get_history_name(name, interval=interval)
    try:
        dates = hget(name=history_name, key="date")
        current_time = time.time() * 1000
        last_candle_time = dates[-1]
        if current_time - last_candle_time > 2 * intervals[interval]:
            set_history(name, interval)
            return load_history(name, interval, num=num + 1)
        data_dict = dict()
        for key in needed_keys:
            data_dict[key] = hget(name=history_name, key=key)
        return data_dict
    except Exception:
        set_history(name, interval)
        return load_history(name, interval, num=num + 1)


def flushall():
    return r.flushall()
