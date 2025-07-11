"""
module tasks:
        read from APIs, add to data base, updateing, and api for reading from data base
"""

import time

import data.backup as backup
import data.redis as redis
from data.models import StockWatch
from finance import oms

symbol_ids = backup.all_ids
wrong_symbol_ids = []
new_group = {}


def create_stock_watch_tables(num=0):
    for i, symbol_id in enumerate(symbol_ids):
        if i >= num:
            print("stock watch for index: {}".format(i))
            info = stock_watch_info(symbol_id)
            if info:
                try:
                    add_stock_watch_table(info)
                except Exception:
                    wrong_symbol_ids.append(
                        dict(id=symbol_id, problem="on save")
                    )


def stock_watch_info(symbol_id, eps=True):
    depth = oms.Binance.get_depth(symbol_id, limit=10)
    int(time.time() * 1000)
    symbol = redis.hget("exchangeInfo", symbol_id)
    data = {
        "InstrumentName": symbol_id,
        "CompanyName": symbol["baseAsset"],
        "depth": [],
    }
    for i in range(10):
        if len(depth["bids"]) > i and len(depth["asks"]) > i:
            level = {
                "bp": float(depth["bids"][i][0]),
                "bq": float(depth["bids"][i][1]),
                "ap": float(depth["asks"][i][0]),
                "aq": float(depth["asks"][i][1]),
            }
            data["depth"].append(level)
    return data


def add_stock_watch_table(info):
    try:
        StockWatch(**info).save()
        print("successful progress")
    except Exception:
        print("This symbol doesn't exist.")


def delete_duplicate():
    for row in StockWatch.objects.all():
        if StockWatch.objects.filter(symbol_id=row.symbol_id).count() > 1:
            row.delete()


class Stock_Watch:
    @staticmethod
    def create_tables():
        create_stock_watch_tables()

    def update(self, num=0):
        update_stock_watch(num)


def update_stock_watch(num=0):
    stocks = StockWatch.objects.all()
    for i, stock in enumerate(stocks):
        if i >= num:
            symbol_id = stock.symbol_id
            print("update stock watch for index: {}".format(i))
            info = stock_watch_info(symbol_id)
            if info:
                try:
                    update_stock_watch_table(stock, info)
                except Exception:
                    wrong_symbol_ids.append(
                        dict(id=symbol_id, problem="on update stock watch")
                    )


def update_stock_watch_table(model, data):
    for key in data:
        model.__setattr__(key, data[key])
    model.save()
    print("{} updated successfully".format(model.instrument_name))
