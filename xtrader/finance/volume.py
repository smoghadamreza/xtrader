from data.redis import load_history


def run_test(data):
    symbol_id = data['symbol_id']
    date = data['index']
    dates = load_history(symbol_id)['date']
    for i, d in enumerate(dates):
        if d > date:
            data['index'] = i
            return buy_volume_decrease(**data)


def buy_volume_decrease(index=0, initial=10000000, symbol_id='IRO1KAVR0001', takeprofit=.3, stoploss=.1):
    stoploss = 1 - stoploss
    history = load_history(symbol_id)
    close = history['close']
    high = history['high']
    date = history['date']
    buy_dates = [date[index]]
    buy = close[index]
    vol = 1
    vol_sum = vol
    margin = initial
    invest = vol * buy
    margin -= invest
    trades_history = [{'price': buy, 'vol': vol, 'action': 'شروع خرید', 'profit': margin - initial, 'day': index}]
    for i, price in enumerate(close[index + 1:]):
        if price < stoploss * buy:
            vol = calc_vol(trades_history, price, takeprofit)
            buy = price
            invest = vol * buy
            vol_sum += vol
            margin -= invest
            buy_dates.append(date[i + index])
            trades_history.append(
                {'price': buy, 'vol': vol, 'action': 'خرید مجدد', 'profit': margin - initial, 'day': i + index})
            if margin < 0:
                print('call margin')
                pass
            continue
        if high[i + index] > (takeprofit + 1) * buy:
            margin += high[i + index] * vol_sum
            trades_history.append(
                {'price': high[i + index], 'vol': vol_sum, 'action': 'فروش و خروج', 'profit': margin - initial, 'day': i + index})
            return {'history': trades_history, 'status': 'worked', 'finishdate': date[i + index], 'dates': buy_dates}
    return {'history': trades_history, 'status': 'running', 'dates': buy_dates}


def calc_vol(history, price, takeprofit=.1):
    loss = 0
    for h in history:
        loss += h['vol'] * (h['price'] - (1 + takeprofit) * price)
    return int(loss / ((takeprofit) * price)) + 1


def test():
    result = {}
    for symbol in ['IRO1KAVR0001', 'IRO1IKCO0001', 'IRO1NAFT0001']:
        result[symbol] = []
        for i in range(100):
            summery = buy_volume_decrease(i, symbol_id=symbol)
            if summery['profit'] < 0:
                result[symbol].append({'i': i, 'margin': summery['profit'], 'action': summery['action']})
    return result
