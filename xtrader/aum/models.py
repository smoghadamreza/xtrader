from datetime import datetime
from typing import List, Dict, Any
from finance.services.exchange.data import TransactionRecord, DepositRecord, WithdrawalRecord

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from utils.unix_millis import UnixMillis
from aum.exception import NameIsTooLong, InvestorAlreadyExists

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

class FundInvestor(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    national_code = models.CharField(
        max_length=20, default="", blank=True, null=True
    )
    phone_number = models.CharField(
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
    
    @classmethod
    def create_investor(cls, fund: Fund, first_name: str, last_name: str, national_code: str):
        if len(first_name) > 20 or len(last_name) > 20:
            raise NameIsTooLong()
        if cls.objects.filter(fund=fund, national_code=national_code).exists():
            raise InvestorAlreadyExists()
        investor = cls.objects.create(
            fund=fund, first_name=first_name,
            last_name=last_name, national_code=national_code
        )
        return investor


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
