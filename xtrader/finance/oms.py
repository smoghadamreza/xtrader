import requests
from django.db import connections
from finance.models import Exchange, TradingView
# from social.models import Follow
from django.conf import settings
from datetime import datetime, timedelta
import threading
import hashlib
import time
import urllib
import hmac
import json
from data import redis


class Binance:
    spot_base = 'https://api.binance.com'

    # try:
    #     data = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()
    # except Exception as e:
    #     data = {'symbols': []}
    # info = {}
    # for symbol in data['symbols']:
    #     if symbol['quoteAsset'] == 'USDT':
    #         info[symbol['symbol']] = symbol
    @staticmethod
    def get_candles(params):
        return requests.get(Binance.spot_base + "/api/v3/klines", params=params).json()

    @staticmethod
    def get_ticker(symbol_id):
        return requests.get(Binance.spot_base + '/api/v3/ticker/24hr', params={'symbol': symbol_id}).json()

    @staticmethod
    def get_bookTicker(symbol_id):
        return requests.get(Binance.spot_base + '/api/v3/ticker/bookTicker', params={'symbol': symbol_id}).json()

    @staticmethod
    def get_depth(symbol_id, limit=10):
        # print(current_time, ticker['E'], current_time - ticker['E'])
        current_time = int(time.time() * 1000)
        try:
            depth = redis.hget('Depth', symbol_id)
            last_depth = depth['lastUpdateTime']
            if current_time - last_depth < 5000:
                return depth
        except Exception as e:
            pass
        depth = requests.get(Binance.spot_base + '/api/v3/depth', params={'symbol': symbol_id, 'limit': limit}).json()
        depth['lastUpdateTime'] = current_time
        redis.hset('Depth', symbol_id, json.dumps(depth))
        return depth

    @staticmethod
    def get_symbol_info(symbol):
        return redis.hget('exchangeInfo', symbol.upper())

    @staticmethod
    def set_symbols():
        exchange_info = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()
        # print("serverTime:", exchange_info['serverTime'])
        for symbol in exchange_info['symbols']:
            # self.symbols.append(symbol['symbol'])
            redis.hset('exchangeInfo', symbol['symbol'], json.dumps(symbol))

    @staticmethod
    def lot_filter(symbol, qty):
        qty = float(qty)
        lot = {}
        for fil in Binance.get_symbol_info(symbol=symbol)['filters']:
            if fil['filterType'] == 'LOT_SIZE':
                lot = fil
                break
        min_qty = float(lot['minQty'])
        max_qty = float(lot['maxQty'])
        step_size = float(lot['stepSize'])
        if qty < min_qty:
            qty = min_qty
        elif qty > max_qty:
            qty = max_qty
        else:
            steps = int(qty / step_size)
            qty = steps * step_size
        baseAssetPrecision = Binance.get_symbol_info(symbol=symbol)['baseAssetPrecision'] - 1
        qty = round(qty, baseAssetPrecision)
        qty = ('{:.' + str(baseAssetPrecision) + 'f}').format(qty)
        return qty

    @staticmethod
    def sign(params, private):
        params['timestamp'] = (int(time.time()) * 1000)
        params['recvWindow'] = 50000
        params_str = urllib.parse.urlencode(params).encode('utf-8')
        sign = hmac.new(
            key=str.encode(private),
            msg=params_str,
            digestmod=hashlib.sha256
        ).hexdigest()
        return params_str.decode("utf-8") + "&signature=" + str(sign)

    @staticmethod
    def get_header(public):
        return {"X-MBX-APIKEY": public, "Content-Type": "application/json"}

    @staticmethod
    def get_orders(ex, symbol):
        # client = Client(ex.public, ex.private)
        # orders = client.get_all_orders(symbol=symbol)
        orders = Binance.get('/api/v3/allOrders', params={'symbol': symbol}, public=ex.public, private=ex.private)
        nonzero = [order for order in orders if float(order['price']) > 0 or order['type'] == 'MARKET'][::-1]
        return nonzero[:15]

    @staticmethod
    def get(endpoint, params={}, public=None, private=None):
        base_url = 'https://api.binance.com'
        url = base_url + endpoint + '?' + Binance.sign(params=params, private=private)
        response = requests.get(url=url, headers=Binance.get_header(public))
        return response.json()

    @staticmethod
    def get_open_orders(ex, symbol):
        return Binance.get('/api/v3/openOrders', params={'symbol': symbol}, public=ex.public, private=ex.private)

    @staticmethod
    def send_order(ex, params):
        order = {
            'symbol': params['symbol'] if 'symbol' in params else params['SymbolId'],
            'quantity': params['quantity'] if 'quantity' in params else params['Quantity'],
        }
        order['quantity'] = Binance.lot_filter(order['symbol'], order['quantity'])
        if 'side' in params:
            order['side'] = params['side'].upper()
        else:
            order['side'] = 'BUY' if params['OrderSide'] == 1 else 'SELL'

        order['type'] = params['type'].upper()
        additional_endpoint = ''
        if params['type'].upper() in ['LIMIT', 'LIMIT_MAKER', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT']:
            order['price'] = params['price'] if 'price' in params else params['Price']
            order['timeInForce'] = 'GTC'
            if params['type'].upper() in ['STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT']:
                order['stopPrice'] = params['stop_price']
        elif params['type'].upper() in ['STOP_LOSS', 'TAKE_PROFIT']:
            order['stopPrice'] = params['stop_price']
        elif params['type'].upper() == 'OCO':
            additional_endpoint = '/oco'
            order['price'] = params['price']
            order['stopPrice'] = params['stop_price']
            order['stopLimitPrice'] = params['stopLimitPrice']
            order['stopLimitTimeInForce'] = 'GTC'
            del order['type']
        else:
            order['type'] = 'MARKET'

        response = requests.post(
            url='https://api.binance.com/api/v3/order{}?'.format(additional_endpoint) + Binance.sign(params=order,
                                                                                                     private=ex.private),
            headers=Binance.get_header(ex.public)).json()
        # print(response)
        result = {'error': True}
        if 'msg' not in response:
            result['error'] = False
        elif response['code'] == -2010:
            result['msg'] = 'موجودی حساب کافی نیست'
        elif response['code'] == -1013:
            result['msg'] = 'تعداد یا قیمت اشتباه وارد شده است'
        elif response['code'] == -1111:
            result['msg'] = 'تعداد یا قیمت اشتباه وارد شده است'
        else:
            result['msg'] = 'لطفا دوباره تلاش کنید کد' + str(response['code'])
        # try:
        #     # result = client.order_limit(**order) if order['type'] == 'LIMIT' else client.order_market(**order)
        #     result = requests.post(url='https://api.binance.com/api/v3/order?'+Binance.sign(params=order, private=ex.private), headers=Binance.get_header(ex.public)).json()
        #     print(result)
        #     result['error'] = False
        # except Exception as e:
        #     if e.code == -2010:
        #         result['msg'] = 'موجودی حساب کافی نیست'
        #     elif e.code == -1013:
        #         result['msg'] = 'تعداد یا قیمت اشتباه وارد شده است'
        #     elif e.code == -1111:
        #         result['msg'] = 'تعداد یا قیمت اشتباه وارد شده است'
        #     else:
        #         result['msg'] = 'لطفا دوباره تلاش کنید کد' + str(e.code)
        # if not result['error'] and followers:
        #     OMSManager.copytrade(protrader_ex=ex, data=order, ex_name='BINANCE', action='order', followers=followers,
        #                          assets=assets, open_orders=open_orders)
        return result

    @staticmethod
    def cancel_order(ex, symbol, order_id):
        # client = Client(ex.public, ex.private)
        try:
            # result = client.cancel_order(symbol=symbol, orderId=int(order_id))
            params = {'symbol': symbol, 'orderId': int(order_id)}
            url = 'https://api.binance.com/api/v3/order?' + Binance.sign(params=params, private=ex.private)
            result = requests.delete(url=url, headers=Binance.get_header(ex.public)).json()
            # followers = Follow.objects.filter(proTrader__trader=ex.trader)
            # if followers:
            #     assets = Binance.get_portfolio(ex)
            #     OMSManager.copytrade(protrader_ex=ex, data={'symbol': symbol}, ex_name='BINANCE', action='cancel',
            #                          followers=followers, assets=assets)
            return result
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def cancel_all_orders(ex, symbol):
        base_url = 'https://api.binance.com'
        url = base_url + '/api/v3/openOrders' + '?' + Binance.sign(params={'symbol': symbol.upper()},
                                                                   private=ex.private)
        response = requests.delete(url=url, headers=Binance.get_header(ex.public))
        for conn in connections.all():
            conn.close()
        return response.json()

    @staticmethod
    def get_balance(ex):
        assets = Binance.get_portfolio(ex)
        if assets is None:
            return None
        return {'BuyingPower': 2000}

    @staticmethod
    def get_portfolio(ex):
        info = Binance.get('/api/v3/account', params={}, public=ex.public, private=ex.private)
        assets = []
        for asset in info['balances']:
            if float(asset['free']) > 0 or float(asset['locked']) > 0:
                assets.append({
                    "symbol": asset['asset'],
                    "free": float(asset['free']),
                    "locked": float(asset['locked']),
                })
        return assets

    @staticmethod
    def verify(public, private):
        account = Binance.get('/api/v3/account', params={}, public=public, private=private)
        return "permissions" in account and "SPOT" in account['permissions']
        # try:
        #     client = Client(public, private)
        #     info = client.get_account()
        #     return True
        # except Exception as e:
        #     return False

    @staticmethod
    def get_daily_snapshots(public, private, limit=30, startTime=None, endTime=None):
        params = {'type': 'SPOT', "limit": limit}
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        return Binance.get('/sapi/v1/accountSnapshot', params=params, public=public, private=private)

    @staticmethod
    def get_deposits(params, public, private, num=0):
        return Binance.get('/wapi/v3/depositHistory.html', params=params, public=public, private=private)

    @staticmethod
    def get_historical_deposits(public, private):
        first_day = datetime.now() - timedelta(days=settings.PERFORMANCE_HISTORY_DAYS)
        step = 89
        deposits = []
        txIds = []
        while first_day < datetime.now():
            end_day = first_day + timedelta(days=step)
            params = {
                'startTime': int(first_day.timestamp() * 1000),
                'endTime': int(end_day.timestamp() * 1000)
            }
            data = Binance.get_deposits(params, public, private)
            # print(data)
            for deposit in data['depositList']:
                txId = deposit['txId']
                if txId not in txIds:
                    txIds.append(txId)
                    deposits.append(deposit)
            first_day += timedelta(days=step)
        return deposits

    @staticmethod
    def get_withdraws(params, public, private):
        return Binance.get('/wapi/v3/withdrawHistory.html', params=params, public=public, private=private)

    @staticmethod
    def get_historical_withdraws(public, private):
        first_day = datetime.now() - timedelta(days=settings.PERFORMANCE_HISTORY_DAYS)
        step = 89
        withdraws = []
        w_ids = []
        while first_day < datetime.now():
            end_day = first_day + timedelta(days=step)
            params = {
                'startTime': int(first_day.timestamp() * 1000),
                'endTime': int(end_day.timestamp() * 1000)
            }
            data = Binance.get_withdraws(params, public, private)
            # print(data)
            for withdraw in data['withdrawList']:
                w_id = withdraw['id']
                if w_id not in w_ids:
                    w_ids.append(w_id)
                    withdraws.append(withdraw)
            first_day += timedelta(days=step)
        return withdraws

    @staticmethod
    def get_trades(params, public, private):
        return Binance.get('/api/v3/myTrades', params=params, public=public, private=private)

    @staticmethod
    def get_historical_trades(symbol, public, private):
        # first_day = datetime.now() - timedelta(days=settings.PERFORMANCE_HISTORY_DAYS)
        from_id = 1
        # step = 89
        trades = []
        t_ids = []
        trades_list = [None]
        while trades_list:
            # end_day = first_day + timedelta(days=step)
            params = {
                'symbol': symbol.upper(),
                'fromId': from_id,
                # 'startTime':int(first_day.timestamp()*1000),
                # 'endTime': int(end_day.timestamp() * 1000)
            }
            trades_list = Binance.get_trades(params, public, private)
            # print(from_id, symbol, trades_list)
            for trade in trades_list:
                t_id = trade['id']
                if t_id not in t_ids:
                    t_ids.append(t_id)
                    trades.append(trade)
                    if t_id > from_id:
                        from_id = t_id + 1
            # first_day += timedelta(days=step)
        return trades

    # @staticmethod
    # def get_full_history(public, private):
    #     history = {
    #         'deposits': Binance.get_historical_deposits(public=public, private=private),
    #         'withdraws': Binance.get_historical_withdraws(public=public, private=private),
    #     }
    #     history = {'trades': {}}
    #
    #     def fetch_history(kind, public, private, symbol=None):
    #         if kind == 'deposits':
    #             history[kind] = Binance.get_historical_deposits(public=public, private=private)
    #         elif kind == 'withdraws':
    #             history[kind] = Binance.get_historical_withdraws(public=public, private=private)
    #         elif kind == 'trades':
    #             history[kind][symbol] = Binance.get_historical_trades(symbol=symbol, public=public, private=private)
    #
    #     threads = [
    #         threading.Thread(target=fetch_history, args=('withdraws', public, private)),
    #         threading.Thread(target=fetch_history, args=('deposits', public, private)),
    #     ]
    #     symbols = ['BTCUSDT', 'ETHUSDT']
    #     for symbol in symbols:
    #         threads.append(threading.Thread(target=fetch_history, args=('trades', public, private, symbol)))
    #     for t in threads:
    #         t.start()
    #     for t in threads:
    #         t.join()
    #     return history

    @staticmethod
    def get_historical_nav(public, private):
        history = []
        endTime = int(time.time() * 1000)
        for _ in range(2):
            snapshots = Binance.get_daily_snapshots(public=public, private=private, endTime=endTime)
            # print(snapshots)
            # print("start:", snapshots['snapshotVos'][0]['updateTime'], "finish:", snapshots['snapshotVos'][-1]['updateTime'])
            history = snapshots['snapshotVos'] + history
            endTime = snapshots['snapshotVos'][0]['updateTime'] - 25 * 60 * 60 * 1000
            # time.sleep(5)
        return history
        # history = Binance.get_full_history(public=public, private=private)
        # actions = Binance.get_actions(history)
        # assets, snapshots = Binance.get_portfo_snapshots(actions)
        # # prices = Binance.get_prices(assets)
        # days = sorted(prices)
        # portfo = {}
        # nav_history = []
        # for idx, day in enumerate(days[:-1]):
        #     if idx == 0:
        #         continue
        #     for snap in snapshots:
        #         if days[idx] <= snap['time'] < days[idx + 1]:
        #             portfo = snap['assets']
        #     if portfo:
        #         nav = portfo.get('USDT', 0)
        #         for asset in assets:
        #             amount = portfo.get(asset)
        #             if amount:
        #                 nav += amount * prices[day][asset]
        #         nav_history.append([day, nav])
        # return nav_history

    @staticmethod
    def get_last_nav(public, private):
        return 0
        # result = Binance.get_daily_snapshots(public=public, private=private)
        # if not result['code'] == 200:
        #     return 0
        # asset_btc = result['snapshotVos'][-1]['data']['totalAssetOfBtc']
        # # assets = list(set([asset['asset'] for asset in balances]))
        # prices = Binance.get_prices(['BTC'])
        # last_day = max(prices)
        # nav = prices[last_day]['BTC'] * float(asset_btc)
        # # for asset in balances:
        # #     if asset['asset'] == 'USDT':
        # #         nav += asset['free'] + asset['locked']
        # #     else:
        # #         nav += prices[last_day][asset['asset']] * (asset['free'] + asset['locked'])
        # return nav

    @staticmethod
    def get_prices(assets):
        data = {}
        for asset in assets:
            if asset == 'USDT':
                continue
            # elif asset[-2:] == 'UP' or asset[-4:] == 'DOWN':
            #     symbol = asset
            else:
                symbol = asset + 'USDT'
            candles = requests.get('https://api.binance.com/api/v3/klines', params={
                'symbol': symbol,
                'interval': '1d',
                'limit': 1000
            }).json()
            for candle in candles:
                t = candle[0]
                if t not in data:
                    data[t] = {}
                data[t][asset] = float(candle[4])
        return data

    @staticmethod
    def get_prices_for_nav(assets):
        data = {}
        for asset in assets:
            if asset != 'USDT':
                price = Binance.get_last_price(asset + 'USDT')
                if price > 0:
                    data[asset] = price
                else:
                    price_btc = Binance.get_last_price(asset + 'BTC')
                    data[asset] = price_btc * Binance.get_last_price('BTCUSDT')
            else:
                data['USDT'] = 1
        return data

    @staticmethod
    def get_last_price(symbol):
        # print("last price", symbol)
        try:
            ticker = redis.hget('LASTPRICE', symbol)
            if ticker['time'] > int(time.time()) - 30:
                return ticker['price']
            raise Exception('lastprice expired ' + symbol)
        except Exception as e:
            tickers = requests.get('https://www.binance.com/api/v3/ticker/price').json()
            found = False
            for ticker in tickers:
                redis.hset('LASTPRICE', ticker['symbol'],
                           json.dumps({'price': float(ticker['price']), 'time': int(time.time())}))
                if ticker['symbol'] == symbol:
                    found = True
                    last_price = float(ticker['price'])
            if not found:
                try:
                    ticker = requests.get('https://www.binance.com/api/v3/ticker/price?symbol={}'.format(symbol)).json()
                    redis.hset('LASTPRICE', ticker['symbol'],
                               json.dumps({'price': float(ticker['price']), 'time': int(time.time())}))
                    last_price = float(ticker['price'])
                except Exception as e:
                    last_price = 0
            return last_price

    @staticmethod
    def get_portfo_snapshots(actions):
        portfo_history = []
        portfo = {'assets': {}}
        assets = []
        for action in actions:
            # print(action)
            if action['action'] == 'deposit':
                asset = action['asset']
                amount = action['amount']
                portfo['assets'][asset] = portfo['assets'].get(asset, 0) + amount
                assets.append(asset)
                # print(action['actionTime'],'deposit', action['amount'], action['asset'])
            elif action['action'] == 'withdraw':
                asset = action['asset']
                amount = action['amount']
                portfo['assets'][asset] -= amount
                # print(action['actionTime'],'withdraw', action['amount'], action['asset'])
            elif action['action'] == 'trade':
                asset = action['symbol'][:-4]
                amount = float(action['qty'])
                value = float(action['quoteQty'])
                if action['isBuyer']:
                    portfo['assets'][asset] = portfo['assets'].get(asset, 0) + amount
                    portfo['assets']['USDT'] = max(portfo['assets']['USDT'] - value, 0)
                    assets.append(asset)
                else:
                    portfo['assets'][asset] = max(portfo['assets'][asset] - amount, 0)
                    portfo['assets']['USDT'] = portfo['assets'].get('USDT', 0) + value
                # print(action['actionTime'], 'trade', 'buy' if action['isBuyer'] else 'sell', action['symbol'], action['qty'], 'value', action['quoteQty'])
            portfo['action'] = action['action']
            portfo['time'] = action['actionTime']
            portfo_history.append(json.dumps(portfo))
        assets = list(set(assets))
        portfo_history = [json.loads(p) for p in portfo_history]
        return [assets, portfo_history]

    @staticmethod
    def get_actions(history):
        events = {}
        for symbol, trades in history['trades'].items():
            for trade in trades:
                trade['action'] = 'trade'
                trade['actionTime'] = trade['time']
                events[trade['time']] = trade
        for deposit in history['deposits']:
            deposit['action'] = 'deposit'
            deposit['actionTime'] = deposit['insertTime']
            events[deposit['insertTime']] = deposit
        for withdraw in history['withdraws']:
            withdraw['action'] = 'withdraw'
            withdraw['actionTime'] = withdraw['applyTime']
            events[withdraw['applyTime']] = withdraw
        return [events[event_time] for event_time in sorted(events)]


class OMSManager:
    exchange_name2obj = {
        'BINANCE': Binance,
    }

    @staticmethod
    def get_exchange(request, trader=None):
        if trader is None:
            trader = request.user
        exchange_obj = None
        exchange_class = None
        exs = Exchange.objects.filter(trader=trader)
        if not exs:
            return exchange_obj, exchange_class
        exchange_obj = exs.first()
        if exchange_obj.name == 'BINANCE':
            exchange_class = Binance
        return exchange_obj, exchange_class

    @staticmethod
    def get_exchanges(request, trader=None):
        if trader is None:
            trader = request.user
        exs = Exchange.objects.filter(trader=trader)
        result = []
        for ex in exs:
            result.append({
                "exchange": ex.exchange,
                "name": ex.name,
                "public": ex.public,
            })
        return result

    @staticmethod
    def get_nav(assets):
        nav = 0
        prices = Binance.get_prices_for_nav(list(set([asset['symbol'] for asset in assets])))
        for asset in assets:
            amount = (asset['free'] + asset['locked'])
            price = prices[asset['symbol']]
            nav += amount * price
        return nav

    @staticmethod
    def order_nav_ratio(new_order, assets, quote_price, order_market_value=0):
        nav = OMSManager.get_nav(assets=assets)
        if order_market_value > 0:
            order_value = order_market_value
        else:
            order_price = new_order['price']
            order_qty = new_order['quantity']
            order_value = order_qty * order_price * quote_price
        return round(order_value / nav, 3)

        # order_side = new_order['side']
        # base_asset = new_order['base']
        # open_orders_values = [
        #     abs(float(open_order['origQty']) - float(open_order['executedQty'])) * float(open_order['price'])
        #     for open_order in open_orders if open_order['side'] == order_side]
        # open_orders_value = sum(open_orders_values) if open_orders_values else 0
        # asset_amount = 0
        # for asset in assets:
        #     if asset['symbol'] == base_asset:
        #         asset_amount += (asset['free'] + asset['locked']) * order_price
        #         break
        # ratio = None
        # if order_side == 'SELL':
        #     if nav:
        #         ratio = (max(asset_amount - open_orders_value - (order_qty * order_price), 0)) / nav
        # elif order_side == 'BUY':
        #     if nav:
        #         ratio = (asset_amount + (order_qty * order_price)) / nav
        # return round(ratio, 3)

    @staticmethod
    def send_followers_order(follower_ex, ratio, order, quote_price):
        new_order = order.copy()
        ex = OMSManager.exchange_name2obj[follower_ex.name]
        assets = ex.get_portfolio(follower_ex)
        # open_orders = Binance.get_open_orders(follower_ex, order['symbol'])
        # order_side = order['side'].upper()
        # open_orders_values = [
        #     abs(float(open_order['origQty']) - float(open_order['executedQty'])) * float(open_order['price'])
        #     for open_order in open_orders if open_order['side'] == order_side]
        # open_orders_value = sum(open_orders_values) if open_orders_values else 0

        nav = OMSManager.get_nav(assets)
        # asset_order = order['base']
        # asset_value = 0
        # for asset in assets:
        #     if asset['symbol'] == asset_order:
        #         asset_value += (asset['free'] + asset['locked']) * order['price']
        #         break
        # value = 0
        # if order_side == 'SELL':
        #     if nav:
        #         value = max(asset_value - open_orders_value - (nav * ratio), 0)
        # elif order_side == 'BUY':
        #     if nav:
        #         value = max((nav * ratio) - asset_value, 0)
        value = max(nav * ratio, 0)
        quantity = value / (order['price'] * quote_price)
        # round(order['quantity'], Binance.info[order['symbol']]['baseAssetPrecision'] - 2)
        if quantity * new_order['price'] * quote_price >= 10:
            new_order['quantity'] = quantity
            ex.send_order(follower_ex, new_order)
        for conn in connections.all():
            conn.close()
            # if not result['error']:

    @staticmethod
    def copytrade(trader, new_order, followers=[], open_orders=[]):
        exchange_followers = Exchange.objects.filter(trader__in=[follower.follower for follower in followers])
        threads = []
        order_action = new_order['x']
        symbol_info = Binance.get_symbol_info(symbol=new_order['s'])
        new_order['base'] = symbol_info['baseAsset']
        new_order['quote'] = symbol_info['quoteAsset']
        quote_price = Binance.get_prices_for_nav([new_order['quote']])[new_order['quote']]
        new_order['side'] = new_order['S'].upper()
        new_order['price'] = float(new_order.get('p', 0))
        new_order['stop_price'] = float(new_order.get('P', 0))
        new_order['stopLimitPrice'] = float(new_order.get('stopLimitPrice', 0))
        new_order['quantity'] = float(new_order['q'])
        new_order['symbol'] = new_order['s']
        new_order['type'] = new_order['o']
        order_market_value = 0
        if new_order['o'] == 'MARKET':
            new_order['price'] = Binance.get_last_price(new_order['s'])
            order_market_value = float(new_order['Q'])
        elif new_order['o'] in ['STOP_LOSS', 'TAKE_PROFIT']:
            new_order['price'] = new_order['stop_price']
            order_market_value = float(new_order['Q'])
        ratio = 0
        if order_action == 'NEW':
            ex_obj, ex_class = OMSManager.get_exchange(None, trader=trader)
            assets = ex_class.get_portfolio(ex_obj)
            ratio = OMSManager.order_nav_ratio(new_order=new_order, assets=assets, quote_price=quote_price,
                                               order_market_value=order_market_value)
        for follower_ex in exchange_followers:
            if order_action == 'NEW':
                threads.append(threading.Thread(
                    target=OMSManager.send_followers_order,
                    args=(follower_ex, ratio, new_order, quote_price)
                )
                )
            elif order_action == 'CANCELED':
                threads.append(
                    threading.Thread(
                        target=OMSManager.exchange_name2obj[follower_ex.name.upper()].cancel_all_orders,
                        args=(follower_ex, new_order['s'])
                    )
                )
            else:
                print('invalid action')
        for t in threads:
            t.start()

    @staticmethod
    def stop_limit_order(price, sprice, side='BUY', quantity=0.001):
        public = 'TZKgcNepxyESKfpmF67rjaSaLHD8DNN68y79wrYFuE62DAfoX90FleriYFatHV15'
        private = 'UtYnWh6Daqc3FG7PbbRokbLGWvjt0ToNUDb504ggxVZOLraYqoiZhBNEaOfVLNHo'
        symbol = 'BTCUSDT'
        order = {
            'price': price,
            'stopPrice': sprice,
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'type': 'STOP_LOSS_LIMIT',
            'timeInForce': 'GTC',
        }
        return requests.post(
            url='https://api.binance.com/api/v3/order?' + Binance.sign(params=order, private=private),
            headers=Binance.get_header(public)).json()

    @staticmethod
    def oco_order(price, sprice, slprice, side='SELL', quantity=0.001):
        public = 'TZKgcNepxyESKfpmF67rjaSaLHD8DNN68y79wrYFuE62DAfoX90FleriYFatHV15'
        private = 'UtYnWh6Daqc3FG7PbbRokbLGWvjt0ToNUDb504ggxVZOLraYqoiZhBNEaOfVLNHo'
        symbol = 'BTCUSDT'
        order = {
            'price': price,
            'stopPrice': sprice,
            'stopLimitPrice': slprice,
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'stopLimitTimeInForce': 'GTC',
        }
        return requests.post(
            url='https://api.binance.com/api/v3/order/oco?' + Binance.sign(params=order, private=private),
            headers=Binance.get_header(public)
        ).json()

    @staticmethod
    def verify_and_create_exchange(trader, name, public, private, exchange):
        if exchange == 'BINANCE':
            if Binance.verify(public=public, private=private):
                if trader:
                    ex = Exchange(trader=trader, name=name, public=public, private=private, exchange=exchange)
                    ex.save()
                return True
        return False

    @staticmethod
    def remove_exchange(trader, ex_name):
        ex = Exchange.objects.filter(trader=trader, name='BINANCE').first()
        if ex:
            tw = TradingView.objects.filter(trader=trader).first()
            if tw:
                if tw.trading:
                    return False
            ex.delete()
        return True
