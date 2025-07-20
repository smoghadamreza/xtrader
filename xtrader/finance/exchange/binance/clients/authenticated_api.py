from abc import abstractmethod
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from typing import Dict, Any, List, Union


from finance.models import Exchange


class AuthenticatedAPIClient:
    BASE_URL = "https://api.binance.com"
    V1_ENDPOINT = "/sapi/v1"
    V3_ENDPOINT = "/api/v3"

    def __init__(self, user_exchange: Exchange):
        self._public_key = user_exchange.public_key
        self._private_key = user_exchange.private_key
        self._trader = user_exchange.trader

    def get(self, endpoint: str, params: dict = {}) -> Union[Dict[str, Any], List[Any]]:
        response = requests.get(
            url=self._create_url(
                endpoint=endpoint,
                params=params
            ),
            headers=self._headers()
        )
        return response.json()

    def post(self, endpoint: str, params: dict) -> Union[Dict[str, Any], List[Any]]:
        response = requests.post(
            url=self._create_url(
                endpoint=endpoint,
                params=params
            ),
            headers=self._headers()
        )
        return response.json()

    def delete(self, endpoint: str, params: dict) -> Union[Dict[str, Any], List[Any]]:
        response = requests.delete(
            url=self._create_url(
                endpoint=endpoint,
                params=params
            ),
            headers=self._headers()
        )
        return response.json()

    def _sign(self, params: dict) -> str:
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = 50000
        query_string = urlencode(params).encode("utf-8")
        signature = hmac.new(
            key=self._private_key.encode(),
            msg=query_string,
            digestmod=hashlib.sha256
        ).hexdigest()
        return f"{query_string.decode()}&signature={signature}"

    def _headers(self):
        return {
            "X-MBX-APIKEY": self._public_key,
            "Content-Type": "application/json",
        }
    
    @abstractmethod
    def _create_url(self, endpoint: str, params: Dict) -> str:
        return f"{self.BASE_URL}{endpoint}?{self._sign(params)}"

