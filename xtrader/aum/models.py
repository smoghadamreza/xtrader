import time
from datetime import datetime
from typing import List, Dict, Any
from datetime import timedelta
from finance.exchange.data import TransactionRecord, DepositRecord, WithdrawalRecord

import requests
from django.contrib.auth.models import User
from django.db import connections, models
from django.utils import timezone
from utils.unix_millis import UnixMillis
from finance import oms
from finance.copy_trade.service import NetAssetValueCalculator

class Fund(models.Model):
    manager = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE
    )
    issue_fee = models.FloatField(default=0.01, blank=True, null=False)
    redeem_fee = models.FloatField(default=0.01, blank=True, null=False)
    fee = models.FloatField(default=0, blank=True, null=False)
    aum = models.FloatField(default=0, blank=True, null=False)
    last_update = models.FloatField(default=0, blank=True, null=True)
    brand = models.CharField(max_length=80, default="", blank=True, null=False)
    deposit = models.FloatField(default=0, blank=True, null=False)
    withdrawal = models.FloatField(default=0, blank=True, null=False)

    def __str__(self):
        return self.brand

    def get_units_count(self):
        result = 0
        investors = FundInvestor.objects.filter(fund=self, units__gt=0).values(
            "units"
        )
        if investors:
            result = investors.aggregate(models.Sum("units"))["units__sum"]
        return result

    def get_assets(self):
        exchange, exchange_class = oms.OMSManager.get_exchange(
            request=None, trader=self.manager
        )
        if exchange_class is None:
            raise ValueError("Exchange class cannot be None")
        return exchange_class.get_portfolio(exchange)

    def get_cash(self, assets=None):
        if not assets:
            assets = self.get_assets()
        usdt = 0
        for asset in assets:
            if asset["symbol"] == "USDT":
                usdt = asset["free"] + asset["locked"]
        self.get_transactions()
        other_assets = self.fee + self.deposit + self.withdraw
        usdt -= other_assets

        nav = NetAssetValueCalculator.calculate_net_asset_value(a)
        self.aum = oms.OMSManager.get_nav(assets=assets) - other_assets
        self.save()
        return usdt

    def get_fund_info(self, float_precision: int = 2) -> Dict[str, int|float|str]:
        round_func = lambda x: round(x, float_precision)
        return {
            "brand": self.brand,
            "aum": round_func(self.aum),
            "manager": self.manager.username,
            "fee": round_func(self.fee),
            "deposit": round_func(self.deposit),
            "withdrawal": round_func(self.withdrawal),
        }
    
    def save_fund_unit_snapshots(self, snapshot_data: Dict[str, Any], asset_quantities: Dict[str, float]):
        for symbol_id, quantity in asset_quantities.items():
            FundUnitSnapshot(
                fund=self,
                asset=symbol_id,
                quantity=quantity,
                value=snapshot_data[symbol_id]["value"],
                ratio=snapshot_data[symbol_id]["ratio"],
                insert_date=snapshot_data["date"],
                age=snapshot_data["age"],
                nav=snapshot_data["nav"],
            ).save()

    def update_fund_balance(self, transactions: List[TransactionRecord]):
        self.deposit = sum(t.amount for t in transactions if t.record_type == DepositRecord)
        self.withdrawal = sum(t.amount for t in transactions if t.record_type == WithdrawalRecord)
        self.last_update = UnixMillis.from_dt_to_ms(dt=datetime.now())
        self.save(update_fields=["deposit", "withdrawal", "last_update"])

    def unit_transfer(self, investor, units, action, value, nav, fee):
        UnitTransfer(
            investor=investor,
            action=action,
            time=timezone.now(),
            units=units,
            value=value,
            commission=fee,
            nav=nav,
        ).save()

    def get_unit_assets(self):
        assets = self.get_assets()
        cash = self.get_cash(assets=assets)
        units = self.get_units_count()
        fund_assets = {
            asset["symbol"]: asset["free"] + asset["locked"]
            for asset in assets
            if not asset["symbol"] == "USDT"
        }
        fund_assets["USDT"] = cash
        return {
            symbol: quantity / units
            for symbol, quantity in fund_assets.items()
        }

    def init_fund_performance(self, history=120):
        snapshots = FundUnitSnapshot.objects.filter(fund=self).order_by("-age")
        if snapshots:
            return "already exists"
        self.create_snapshots(assets=self.get_unit_assets(), history=history)
        return "created"

    def fund_daily_snapshot(self):
        snapshot = (
            FundUnitSnapshot.objects.filter(fund=self)
            .order_by("-age")
            .values("age", "insert_date")
            .first()
        )

        if snapshot is None:
            raise ValueError("FundUnitSnapshot not found")

        insert_date = timezone.datetime.today()
        if str(snapshot["insert_date"]) == str(insert_date.date()):
            print("snapshot exists!")
            return None
        age = snapshot["age"] + 1
        unit_assets = self.get_unit_assets()
        prices = oms.Binance.get_prices_for_nav(unit_assets)
        nav = sum(
            [
                prices[asset] * quantity
                for asset, quantity in unit_assets.items()
            ]
        )
        for asset, quantity in unit_assets.items():
            value = quantity * prices[asset]
            ratio = value / nav
            FundUnitSnapshot(
                fund=self,
                asset=asset,
                quantity=quantity,
                value=value,
                ratio=ratio,
                insert_date=insert_date,
                age=age,
                nav=nav,
            ).save()

    @classmethod
    def get_daily_snapshots(cls):
        funds = cls.objects.all()
        for fund in funds:
            if FundUnitSnapshot.objects.filter(fund=fund).first():
                fund.fund_daily_snapshot()
            else:
                fund.init_fund_performance()
        for conn in connections.all():
            conn.close()

    def get_fund_performance(self, mode="all", history=120):
        snapshots = (
            FundUnitSnapshot.objects.filter(fund=self)
            .order_by("age")
            .values("age", "nav", "insert_date")
        )
        age = -1
        pnav = None
        result = []
        for snapshot in snapshots:
            if not snapshot["age"] > age:
                continue
            age += 1
            if pnav is None:
                pnav = snapshot["nav"]
                continue
            r = (snapshot["nav"] / pnav) - 1
            pnav = snapshot["nav"]
            result.append(
                {
                    "age": snapshot["age"],
                    "nav": round(snapshot["nav"], 2),
                    "date": snapshot["insert_date"],
                    "return": 100 * round(r, 3),
                }
            )
        result = result[-history:]
        if mode == "fund":
            return [
                [int(1000 * time.mktime(r["date"].timetuple())), r["nav"]]
                for r in result
            ]
        btc_candles = requests.get(
            "https://api.binance.com/api/v3/klines",
            params={"symbol": "BTCUSDT", "interval": "1d", "limit": 500},
        ).json()
        btc_prices = [float(c[4]) for c in btc_candles[-len(result) - 2 : -1]]
        try:
            p_price = btc_prices[0]  # Initialize with first price
            for idx, price in enumerate(
                btc_prices[1:], start=1
            ):  # Skip first element
                result[idx - 1]["btc"] = price
                result[idx - 1]["btcReturn"] = 100 * round(
                    (price / p_price) - 1, 3
                )
                p_price = price
        except IndexError:
            raise ValueError("btc_prices cannot be empty")
        if mode == "btc":
            return [
                [int(1000 * time.mktime(r["date"].timetuple())), r["btc"]]
                for r in result
            ]
        return {"data": result[::-1]}


class FundInvestor(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    nationalCode = models.CharField(
        max_length=20, default="", blank=True, null=True
    )
    phoneNumber = models.CharField(
        max_length=20, default="", blank=True, null=True
    )
    first_name = models.CharField(
        max_length=20, default="", blank=True, null=False
    )
    last_name = models.CharField(
        max_length=20, default="", blank=True, null=False
    )
    note = models.CharField(max_length=20, default="", blank=True, null=True)
    units = models.FloatField(default=0, blank=True, null=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class UnitTransfer(models.Model):
    investor = models.ForeignKey(FundInvestor, on_delete=models.CASCADE)
    action = models.CharField(max_length=12, null=True, blank=True)
    time = models.DateTimeField(blank=True, null=True)
    units = models.FloatField(default=0, blank=True, null=True)
    nav = models.FloatField(default=0, blank=True, null=True)
    value = models.FloatField(default=0, blank=True, null=True)
    commission = models.FloatField(default=0, blank=True, null=True)


class FundUnitSnapshot(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    asset = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.FloatField(default=0, null=True, blank=True)
    value = models.FloatField(default=0, null=True, blank=True)
    nav = models.FloatField(default=0, null=True, blank=True)
    ratio = models.FloatField(default=0, null=True, blank=True)
    insert_date = models.DateField(default=None, null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)
