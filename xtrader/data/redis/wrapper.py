import json
from typing import (
    cast, Any, Dict, Tuple, Optional, Union, List, Set, Mapping, Sequence
)

import redis
from django.conf import settings
from finance.exchange.data import SymbolInfo
from data.redis.constants import RedisNameSpace
import logging



logger = logging.getLogger(__name__)

JSONType = Union[
    str, int, float, bool, None,
    Sequence["JSONType"],
    Mapping[str, "JSONType"]
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

    def hget_symbol_info(self, symbol_id: str) -> SymbolInfo:
        symbol_info_data = self.hget(
            namespace=RedisNameSpace.EXCHANGE_INFO, key=symbol_id
        )
        return SymbolInfo.from_dict(data=symbol_info_data)

    def hget_all_symbol_info(self) -> Dict[str, SymbolInfo]:
        symbol_info_data_dict = self.hgetall(key=RedisNameSpace.EXCHANGE_INFO)
        result = {}
        for symbol_id, symbol_info_data in symbol_info_data_dict.items():
            result[symbol_id] = SymbolInfo.from_dict(data=symbol_info_data)
        return result
    
    def add_symbols(self, symbol_ids: List[str]) -> None:
        """Store all symbol_ids into the Redis set under SYMBOLS namespace."""
        if not symbol_ids:
            return
        # unpack list into *args
        self._redis.sadd(RedisNameSpace.SYMBOLS, *symbol_ids)

    def get_all_symbol_ids(self) -> List[str]:
        """Retrieve all symbol_ids from Redis set (decode bytes to str)."""
        raw_symbols = cast(
            typ=Set[bytes],
            val=self._redis.smembers(RedisNameSpace.SYMBOLS)
        )
        return [s.decode("utf-8") for s in raw_symbols]
    
    @staticmethod
    def _dump_value(value: JSONType) -> Tuple[str, bool]:
        try:
            value_str: str = json.dumps(value)
        except TypeError:
            logger.exception(f"tried to set invalid data type {type(value)} into redis")
            return "", False
        return value_str, True
    

redis_wrapper = RedisWrapper()
