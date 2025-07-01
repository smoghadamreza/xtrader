"""
module tasks:
        read from APIs, add to data base, updateing, and api for reading from data base
"""

import time

from data import backup, redis
from data.models import StockWatch
from finance import oms

symbol_ids = backup.all_ids
wrong_symbol_ids = []
new_group = {}


def createStockWatchTables(num=0):
    for i, symbol_id in enumerate(symbol_ids):
        if i >= num:
            print("stock watch for index: {}".format(i))
            info = stockWatchInfo(symbol_id)
            if info:
                try:
                    addStockWatchTable(info)
                except Exception:
                    wrong_symbol_ids.append(
                        dict(id=symbol_id, problem="on save")
                    )


def stockWatchInfo(symbol_id, eps=True):
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


def addStockWatchTable(info):
    try:
        StockWatch(**info).save()
        print("successful progress")
    except Exception:
        print("This symbol doesn't exist.")


def cleanduplicate():
    for row in StockWatch.objects.all():
        if StockWatch.objects.filter(SymbolId=row.SymbolId).count() > 1:
            row.delete()


class Stock_Watch:
    @staticmethod
    def create_tables():
        createStockWatchTables()

    def update(self, num=0):
        update_stock_watch(num)


def update_stock_watch(num=0):
    stocks = StockWatch.objects.all()
    for i, stock in enumerate(stocks):
        if i >= num:
            symbol_id = stock.SymbolId
            print("update stock watch for index: {}".format(i))
            info = stockWatchInfo(symbol_id)
            if info:
                try:
                    updateStockWatchTable(stock, info)
                except Exception:
                    wrong_symbol_ids.append(
                        dict(id=symbol_id, problem="on update stock watch")
                    )


def updateStockWatchTable(model, data):
    for key in data:
        model.__setattr__(key, data[key])
    model.save()
    print("{} updated successfully".format(model.InstrumentName))
