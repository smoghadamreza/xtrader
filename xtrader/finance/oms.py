import hashlib
import hmac
import json
import threading
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.db import connections
from django.contrib.auth.models import User
from finance.services.exchange.factory import ExchangeServiceFactory

import data.redis as redis
from finance.models import Exchange, TradingView

class Binance:
    spot_base = "https://api.binance.com"

    @staticmethod
    def get_candles(params):
        return requests.get(
            Binance.spot_base + "/api/v3/klines", params=params
        ).json()

    @staticmethod
    def get_ticker(symbol_id):
        return requests.get(
            Binance.spot_base + "/api/v3/ticker/24hr",
            params={"symbol": symbol_id},
        ).json()

    @staticmethod
    def get_bookTicker(symbol_id):
        return requests.get(
            Binance.spot_base + "/api/v3/ticker/bookTicker",
            params={"symbol": symbol_id},
        ).json()

    @staticmethod
    def get_depth(symbol_id, limit=10):
        current_time = int(time.time() * 1000)
        try:
            depth = redis.hget("Depth", symbol_id)
            last_depth = depth["lastUpdateTime"]
            if current_time - last_depth < 5000:
                return depth
        except Exception:
            pass
        depth = requests.get(
            Binance.spot_base + "/api/v3/depth",
            params={"symbol": symbol_id, "limit": limit},
        ).json()
        depth["lastUpdateTime"] = current_time
        redis.hset("Depth", symbol_id, json.dumps(depth))
        return depth

    @staticmethod
    def get_symbol_info(symbol):
        return redis.hget("exchangeInfo", symbol.upper())

    @staticmethod
    def set_symbols():
        exchange_info = requests.get(
            "https://api.binance.com/api/v3/exchangeInfo"
        ).json()
        for symbol in exchange_info["symbols"]:
            redis.hset("exchangeInfo", symbol["symbol"], json.dumps(symbol))

    @staticmethod
    def lot_filter(symbol, qty):
        qty = float(qty)
        lot = {}
        for fil in Binance.get_symbol_info(symbol=symbol)["filters"]:
            if fil["filterType"] == "LOT_SIZE":
                lot = fil
                break
        min_qty = float(lot["minQty"])
        max_qty = float(lot["maxQty"])
        step_size = float(lot["stepSize"])
        if qty < min_qty:
            qty = min_qty
        elif qty > max_qty:
            qty = max_qty
        else:
            steps = int(qty / step_size)
            qty = steps * step_size
        baseAssetPrecision = (
            Binance.get_symbol_info(symbol=symbol)["baseAssetPrecision"] - 1
        )
        qty = round(qty, baseAssetPrecision)
        qty = ("{:." + str(baseAssetPrecision) + "f}").format(qty)
        return qty

    @staticmethod
    def sign(params, private):
        params["timestamp"] = int(time.time()) * 1000
        params["recvWindow"] = 50000
        params_str = urlencode(params).encode("utf-8")
        sign = hmac.new(
            key=str.encode(private), msg=params_str, digestmod=hashlib.sha256
        ).hexdigest()
        return params_str.decode("utf-8") + "&signature=" + str(sign)

    @staticmethod
    def get_header(public):
        return {"X-MBX-APIKEY": public, "Content-Type": "application/json"}

    @staticmethod
    def get_orders(ex, symbol):
        orders = Binance.get(
            "/api/v3/allOrders",
            params={"symbol": symbol},
            public=ex.public,
            private=ex.private,
        )
        nonzero = [
            order
            for order in orders
            if float(order["price"]) > 0 or order["type"] == "MARKET"
        ][::-1]
        return nonzero[:15]

    @staticmethod
    def get(endpoint, params={}, public=None, private=None):
        base_url = "https://api.binance.com"
        url = (
            base_url
            + endpoint
            + "?"
            + Binance.sign(params=params, private=private)
        )
        response = requests.get(url=url, headers=Binance.get_header(public))
        return response.json()

    @staticmethod
    def get_open_orders(ex, symbol):
        return Binance.get(
            "/api/v3/openOrders",
            params={"symbol": symbol},
            public=ex.public,
            private=ex.private,
        )

    @staticmethod
    def send_order(ex, params):
        order = {
            "symbol": (
                params["symbol"] if "symbol" in params else params["SymbolId"]
            ),
            "quantity": (
                params["quantity"]
                if "quantity" in params
                else params["Quantity"]
            ),
        }
        order["quantity"] = Binance.lot_filter(
            order["symbol"], order["quantity"]
        )
        if "side" in params:
            order["side"] = params["side"].upper()
        else:
            order["side"] = "BUY" if params["OrderSide"] == 1 else "SELL"

        order["type"] = params["type"].upper()
        additional_endpoint = ""
        if params["type"].upper() in [
            "LIMIT",
            "LIMIT_MAKER",
            "STOP_LOSS_LIMIT",
            "TAKE_PROFIT_LIMIT",
        ]:
            order["price"] = (
                params["price"] if "price" in params else params["Price"]
            )
            order["timeInForce"] = "GTC"
            if params["type"].upper() in [
                "STOP_LOSS_LIMIT",
                "TAKE_PROFIT_LIMIT",
            ]:
                order["stopPrice"] = params["stop_price"]
        elif params["type"].upper() in ["STOP_LOSS", "TAKE_PROFIT"]:
            order["stopPrice"] = params["stop_price"]
        elif params["type"].upper() == "OCO":
            additional_endpoint = "/oco"
            order["price"] = params["price"]
            order["stopPrice"] = params["stop_price"]
            order["stopLimitPrice"] = params["stopLimitPrice"]
            order["stopLimitTimeInForce"] = "GTC"
            del order["type"]
        else:
            order["type"] = "MARKET"

        response = requests.post(
            url="https://api.binance.com/api/v3/order{}?".format(
                additional_endpoint
            )
            + Binance.sign(params=order, private=ex.private),
            headers=Binance.get_header(ex.public),
        ).json()
        result: dict[str, bool | str] = {"error": True}
        if "msg" not in response:
            result["error"] = False

        elif response["code"] == -2010:
            result["msg"] = "موجودی حساب کافی نیست"
        elif response["code"] == -1013:
            result["msg"] = "تعداد یا قیمت اشتباه وارد شده است"
        elif response["code"] == -1111:
            result["msg"] = "تعداد یا قیمت اشتباه وارد شده است"
        else:
            result["msg"] = "لطفا دوباره تلاش کنید کد" + str(response["code"])
        return result

    @staticmethod
    def cancel_order(ex, symbol, order_id):
        try:
            params = {"symbol": symbol, "orderId": int(order_id)}
            url = "https://api.binance.com/api/v3/order?" + Binance.sign(
                params=params, private=ex.private
            )
            result = requests.delete(
                url=url, headers=Binance.get_header(ex.public)
            ).json()
            return result
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def cancel_all_orders(ex, symbol):
        base_url = "https://api.binance.com"
        url = (
            base_url
            + "/api/v3/openOrders"
            + "?"
            + Binance.sign(
                params={"symbol": symbol.upper()}, private=ex.private
            )
        )
        response = requests.delete(
            url=url, headers=Binance.get_header(ex.public)
        )
        for conn in connections.all():
            conn.close()
        return response.json()

    @staticmethod
    def get_balance(ex) -> dict:
        assets = Binance.get_portfolio(ex)
        if assets is None:
            return {"buying_power": 0}
        return {"buying_power": 2000}

    @staticmethod
    def get_portfolio(ex):
        info = Binance.get(
            "/api/v3/account", params={}, public=ex.public, private=ex.private
        )
        assets = []
        for asset in info["balances"]:
            if float(asset["free"]) > 0 or float(asset["locked"]) > 0:
                assets.append(
                    {
                        "symbol": asset["asset"],
                        "free": float(asset["free"]),
                        "locked": float(asset["locked"]),
                    }
                )
        return assets

    @staticmethod
    def verify(public, private):
        account = Binance.get(
            "/api/v3/account", params={}, public=public, private=private
        )
        return "permissions" in account and "SPOT" in account["permissions"]

    @staticmethod
    def get_daily_snapshots(
        public, private, limit=30, startTime=None, endTime=None
    ):
        params = {"type": "SPOT", "limit": limit}
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
        return Binance.get(
            "/sapi/v1/accountSnapshot",
            params=params,
            public=public,
            private=private,
        )

    @staticmethod
    def get_deposits(params, public, private, num=0):
        return Binance.get(
            "/wapi/v3/depositHistory.html",
            params=params,
            public=public,
            private=private,
        )

    @staticmethod
    def get_historical_deposits(public, private):
        first_day = datetime.now() - timedelta(
            days=settings.PERFORMANCE_HISTORY_DAYS
        )
        step = 89
        deposits = []
        txIds = []
        while first_day < datetime.now():
            end_day = first_day + timedelta(days=step)
            params = {
                "startTime": int(first_day.timestamp() * 1000),
                "endTime": int(end_day.timestamp() * 1000),
            }
            data = Binance.get_deposits(params, public, private)
            for deposit in data["depositList"]:
                txId = deposit["txId"]
                if txId not in txIds:
                    txIds.append(txId)
                    deposits.append(deposit)
            first_day += timedelta(days=step)
        return deposits

    @staticmethod
    def get_withdraws(params, public, private):
        return Binance.get(
            "/wapi/v3/withdrawHistory.html",
            params=params,
            public=public,
            private=private,
        )

    @staticmethod
    def get_historical_withdraws(public, private):
        first_day = datetime.now() - timedelta(
            days=settings.PERFORMANCE_HISTORY_DAYS
        )
        step = 89
        withdraws = []
        w_ids = []
        while first_day < datetime.now():
            end_day = first_day + timedelta(days=step)
            params = {
                "startTime": int(first_day.timestamp() * 1000),
                "endTime": int(end_day.timestamp() * 1000),
            }
            data = Binance.get_withdraws(params, public, private)
            for withdraw in data["withdrawList"]:
                w_id = withdraw["id"]
                if w_id not in w_ids:
                    w_ids.append(w_id)
                    withdraws.append(withdraw)
            first_day += timedelta(days=step)
        return withdraws

    @staticmethod
    def get_trades(params, public, private):
        return Binance.get(
            "/api/v3/myTrades", params=params, public=public, private=private
        )

    @staticmethod
    def get_historical_trades(symbol, public, private):
        from_id = 1
        trades = []
        t_ids = []
        trades_list = [None]
        while trades_list:
            params = {
                "symbol": symbol.upper(),
                "fromId": from_id,
            }
            trades_list = Binance.get_trades(params, public, private)
            for trade in trades_list:
                t_id = trade["id"]
                if t_id not in t_ids:
                    t_ids.append(t_id)
                    trades.append(trade)
                    if t_id > from_id:
                        from_id = t_id + 1
        return trades

    @staticmethod
    def get_historical_nav(public, private):
        history = []
        endTime = int(time.time() * 1000)
        for _ in range(2):
            snapshots = Binance.get_daily_snapshots(
                public=public, private=private, endTime=endTime
            )
            history = snapshots["snapshotVos"] + history
            endTime = (
                snapshots["snapshotVos"][0]["updateTime"] - 25 * 60 * 60 * 1000
            )
        return history

    @staticmethod
    def get_prices_for_nav(assets):
        data = {}
        for asset in assets:
            if asset != "USDT":
                price = Binance.get_last_price(asset + "USDT")
                if price > 0:
                    data[asset] = price
                else:
                    price_btc = Binance.get_last_price(asset + "BTC")
                    data[asset] = price_btc * Binance.get_last_price("BTCUSDT")
            else:
                data["USDT"] = 1
        return data

    @staticmethod
    def get_last_price(symbol):
        last_price = 0
        try:
            ticker = redis.hget("LASTPRICE", symbol)
            if ticker["time"] > int(time.time()) - 30:
                return ticker["price"]
            raise Exception("lastprice expired " + symbol)
        except Exception:
            tickers = requests.get(
                "https://www.binance.com/api/v3/ticker/price"
            ).json()
            found = False
            for ticker in tickers:
                redis.hset(
                    "LASTPRICE",
                    ticker["symbol"],
                    json.dumps(
                        {
                            "price": float(ticker["price"]),
                            "time": int(time.time()),
                        }
                    ),
                )
                if ticker["symbol"] == symbol:
                    found = True
                    last_price = float(ticker["price"])
            if not found:
                try:
                    ticker = requests.get(
                        "https://www.binance.com/api/v3/ticker/price?symbol={}".format(
                            symbol
                        )
                    ).json()
                    redis.hset(
                        "LASTPRICE",
                        ticker["symbol"],
                        json.dumps(
                            {
                                "price": float(ticker["price"]),
                                "time": int(time.time()),
                            }
                        ),
                    )
                    last_price = float(ticker["price"])
                except Exception:
                    last_price = 0
            return last_price

class OMSManager:
    exchange_name_to_class = {
        "BINANCE": Binance,
    }

    @staticmethod
    def get_exchange(request, trader=None):
        if trader is None:
            trader = request.user
        trader_exchange = None
        exchange_class = None
        exchanges = Exchange.objects.filter(trader=trader)
        if not exchanges.exists():
            return trader_exchange, exchange_class

        trader_exchange = exchanges.first()
        if trader_exchange is None:
            raise ValueError("Exchange object cannot be None")
        if trader_exchange.name == "BINANCE":
            exchange_class = Binance
        return trader_exchange, exchange_class

    @staticmethod
    def get_exchanges(request, trader=None):
        if trader is None:
            trader = request.user
        exs = Exchange.objects.filter(trader=trader)
        result = []
        for ex in exs:
            result.append(
                {
                    "exchange": ex.exchange,
                    "name": ex.name,
                    "public": ex.public,
                }
            )
        return result

    @staticmethod
    def get_nav(assets):
        nav = 0
        prices = Binance.get_prices_for_nav(
            list(set([asset["symbol"] for asset in assets]))
        )
        for asset in assets:
            amount = asset["free"] + asset["locked"]
            price = prices[asset["symbol"]]
            nav += amount * price
        return nav

    @staticmethod
    def order_nav_ratio(
        new_order, assets, quote_price, order_market_value: float = 0.0
    ):
        nav = OMSManager.get_nav(assets=assets)
        if order_market_value > 0:
            order_value = order_market_value
        else:
            order_price = new_order["price"]
            order_qty = new_order["quantity"]
            order_value = order_qty * order_price * quote_price
        return round(order_value / nav, 3)

    @staticmethod


    @staticmethod
    def copy_trade(trader, new_order, followers=[], open_orders=[]):
        exchange_followers = Exchange.objects.filter(
            trader__in=[follower.follower for follower in followers]
        )
        threads = []
        order_action = new_order["x"]
        symbol_info = Binance.get_symbol_info(symbol=new_order["s"])
        new_order["base"] = symbol_info["baseAsset"]
        new_order["quote"] = symbol_info["quoteAsset"]
        quote_price = Binance.get_prices_for_nav([new_order["quote"]])[
            new_order["quote"]
        ]
        new_order["side"] = new_order["S"].upper()
        new_order["price"] = float(new_order.get("p", 0))
        new_order["stop_price"] = float(new_order.get("P", 0))
        new_order["stopLimitPrice"] = float(new_order.get("stopLimitPrice", 0))
        new_order["quantity"] = float(new_order["q"])
        new_order["symbol"] = new_order["s"]
        new_order["type"] = new_order["o"]
        order_market_value = 0
        if new_order["o"] == "MARKET":
            new_order["price"] = Binance.get_last_price(new_order["s"])
            order_market_value = float(new_order["Q"])
        elif new_order["o"] in ["STOP_LOSS", "TAKE_PROFIT"]:
            new_order["price"] = new_order["stop_price"]
            order_market_value = float(new_order["Q"])
        ratio = 0
        if order_action == "NEW":
            exchange, exchange_class = OMSManager.get_exchange(
                None, trader=trader
            )
            if exchange_class is None:
                raise ValueError("Exchange class cannot be None")
            assets = exchange_class.get_portfolio(exchange)
            ratio = OMSManager.order_nav_ratio(
                new_order=new_order,
                assets=assets,
                quote_price=quote_price,
                order_market_value=order_market_value,
            )
        for follower_ex in exchange_followers:
            if order_action == "NEW":
                threads.append(
                    threading.Thread(
                        target=OMSManager.send_followers_order,
                        args=(follower_ex, ratio, new_order, quote_price),
                    )
                )
            elif order_action == "CANCELED":
                threads.append(
                    threading.Thread(
                        target=OMSManager.exchange_name_to_class[
                            follower_ex.name.upper()
                        ].cancel_all_orders,
                        args=(follower_ex, new_order["s"]),
                    )
                )
            else:
                print("invalid action")
        for t in threads:
            t.start()

    @staticmethod
    def verify_and_create_exchange(trader, name, public, private, exchange):
        if exchange == "BINANCE":
            if Binance.verify(public=public, private=private):
                if trader:
                    ex = Exchange(
                        trader=trader,
                        name=name,
                        public=public,
                        private=private,
                        exchange=exchange,
                    )
                    ex.save()
                return True
        return False

    

class XtraderExchangeService:

    @staticmethod
    def remove_exchange(trader: User, name: str) -> bool:
        exchange = Exchange.objects.filter(trader=trader, name=name)
        if not exchange.exists():
            return False
        
        trading_vieww = TradingView.objects.filter(trader=trader)
        if trading_vieww.exists():
            return False
        
        exchange.delete()
        return True
    
    @staticmethod
    def verify_and_create_exchange(trader: User, kwargs: dict) -> bool:
        valid_fields = {k: v for k, v in kwargs.items() if hasattr(Exchange, k)}
        exchange = Exchange.objects.create(trader=trader, **valid_fields)
        exchange_service = ExchangeServiceFactory.get_service(exchange=exchange)
        if exchange_service.has_spot_trading_permission():
            return True
        exchange.delete()
        return False
    

xtrader_exchange_service = XtraderExchangeService()
