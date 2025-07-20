import json
import time
from typing import cast, Any, Dict, Tuple, Optional, Union, List

import redis
import requests
from django.conf import settings

import logging


logger = logging.getLogger(__name__)

JSONPrimitive = Union[str, int, float, bool, None]
JSONType = Union[
    JSONPrimitive,
    List["JSONType"],
    Dict[str, "JSONType"]
]

class RedisWrapper:
    def __init__(self) -> None:
        self._redis = redis.Redis(host="redis", port=6379, db=settings.REDIS_DB)

    def hgetall(self, key: str) -> Dict[str, Any]:
        result = cast(dict, self._redis.hgetall(name=key))
        return {k.decode(): v.decode() for k, v in result.items()}

    def hset(self, namespace: str, key: str, value: JSONType) -> int:
        value_str, success = self._dump_value(value=value)
        if not success:
            return -1
        result = cast(int, self._redis.hset(name=namespace, key=key, value=value_str))
        return result
    
    def hsetex(
            self, namespace: str, key: str, value: JSONType,
            ttl: Optional[int],  # in seconds
        ) -> int:
        value_str, success = self._dump_value(value=value)
        if not success:
            return -1
        result = cast(int, self._redis.hsetex(name=namespace, key=key, value=value_str, ex=ttl))
        return result

    def hget(self, namespace: str, key: str) -> dict:
        value = cast(bytes, self._redis.hget(name=namespace, key=key))
        if value is None:
            return {}

        return json.loads(value.decode())

    def keys(self):
        return self._redis.keys()

    @staticmethod
    def _dump_value(value: JSONType) -> Tuple[str, bool]:
        try:
            value_str: str = json.dumps(value)
        except TypeError:
            logger.exception(f"tried to set invalid data type {type(value)} into redis")
            return "", False
        return value_str, True


redis_wrapper = RedisWrapper()


needed_keys = ["date", "open", "high", "low", "close", "volume"]
intervals = settings.INTERVALS
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
