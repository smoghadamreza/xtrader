from django.db import models
from django.contrib.auth.models import User
from finance import oms
import time
from datetime import timedelta
import requests
from django.utils import timezone
from django.db import connections


# Create your models here.
class Fund(models.Model):
    manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    issue_fee = models.FloatField(default=0.01, blank=True, null=True)
    redeem_fee = models.FloatField(default=0.01, blank=True, null=True)
    # units = models.FloatField(default=0, blank=True, null=True)
    fee = models.FloatField(default=0, blank=True, null=True)
    aum = models.FloatField(default=0, blank=True, null=True)
    last_update = models.FloatField(default=0, blank=True, null=True)
    brand = models.CharField(max_length=80, default='', blank=True, null=True)
    deposit = models.FloatField(default=0, blank=True, null=True)
    withdraw = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.brand

    def get_units_count(self):
        result = 0
        investors = FundInvestor.objects.filter(fund=self, units__gt=0).values('units')
        if investors:
            result = investors.aggregate(models.Sum('units'))['units__sum']
        return result

    def get_assets(self):
        exchange_obj, exchange_class = oms.OMSManager.get_exchange(request=None, trader=self.manager)
        return exchange_class.get_portfolio(exchange_obj)

    def get_cash(self, assets=None):
        if not assets:
            assets = self.get_assets()
        usdt = 0
        for asset in assets:
            if asset['symbol'] == 'USDT':
                usdt = asset['free'] + asset['locked']
        self.get_transactions()
        other_assets = self.fee + self.deposit + self.withdraw
        usdt -= other_assets
        self.aum = oms.OMSManager.get_nav(assets=assets) - other_assets
        # self.last_update = datetime.now()
        self.save()
        return usdt

    def get_fund_info(self):
        cash = self.get_cash()
        units = self.get_units_count()
        nav = 0
        if units:
            nav = round(self.aum / units, 2)
        result = {
            'brand': self.brand,
            'units': units,
            'cash': round(cash, 2),
            'aum': round(self.aum, 2),
            'manager': self.manager.username,
            'nav': nav,
            'fee': round(self.fee, 2),
            'issue': round((1 + self.issue_fee) * nav, 2),
            'redeem': round((1 - self.redeem_fee) * nav, 2),
            'deposit': round(self.deposit, 2),
            'withdraw': round(self.withdraw, 2),
        }
        return result

    def get_transactions(self):
        ex_obj, ex = oms.OMSManager.get_exchange(request=None, trader=self.manager)

        d = []
        deposits = d + oms.Binance.get_deposits(params={'asset': 'USDT'}, public=ex_obj.public, private=ex_obj.private)[
            'depositList']
        withdraws = oms.Binance.get_withdraws(params={'asset': 'USDT'}, public=ex_obj.public, private=ex_obj.private)[
            'withdrawList']
        trxs = {}
        for deposit in deposits:
            trxs[deposit['insertTime']] = {
                'time': deposit['insertTime'],
                'amount': float(deposit['amount']),
                'action': 'واریز',
                'trx': 'deposit',
            }
        for withdraw in withdraws:
            trxs[withdraw['applyTime']] = {
                'time': withdraw['applyTime'],
                'amount': float(withdraw['amount']),
                'action': 'برداشت',
                'trx': 'withdraw',
            }
        result = []
        for trx_time in sorted(trxs):
            result.append(trxs[trx_time])
            if trxs[trx_time]['trx'] == 'deposit' and trx_time > self.last_update:
                self.deposit += trxs[trx_time]['amount']
                self.last_update = int(time.time() * 1000)
                self.save()
        return result

    def issue_redeem(self, investor, params):
        fund_info = self.get_fund_info()
        nav = fund_info['nav']
        units = params.get('amount', None)

        result = {}
        if params['action'] == 'issue':
            issue_nav = fund_info['issue']
            if self.deposit >= units * issue_nav:
                investor.units += units
                value = units * issue_nav
                self.deposit -= value
                fee = units * (issue_nav - nav)
                self.fee += fee
                self.last_update = int(time.time() * 1000)
                self.unit_transfer(investor=investor, units=units, action=params['action'], nav=nav, value=value,
                                   fee=fee)
                result['c'] = 200
            else:
                result['msg'] = 'موجودی واریزی صندوق کافی نیست'
        elif params['action'] == 'redeem':
            redeem_nav = fund_info['redeem']
            if investor.units >= units:
                investor.units -= units
                value = units * redeem_nav
                self.withdraw += value
                fee = units * (nav - redeem_nav)
                self.fee += fee
                self.last_update = int(time.time() * 1000)
                self.unit_transfer(investor=investor, units=units, action=params['action'], value=value, nav=nav,
                                   fee=fee)
                result['c'] = 200
            else:
                result['msg'] = 'سرمایه‌گذار واحد‌های کمتری دارد'
        else:
            result['msg'] = 'عملیات مشخص نشده است'
        return result

    @staticmethod
    def unit_transfer(investor, units, action, value, nav, fee):
        UnitTransfer(investor=investor,
                     action=action, time=timezone.now(), units=units,
                     value=value, commission=fee, nav=nav
                     ).save()

    def get_unit_assets(self):
        assets = self.get_assets()
        cash = self.get_cash(assets=assets)
        units = self.get_units_count()
        fund_assets = {asset['symbol']: asset['free'] + asset['locked'] for asset in assets if
                       not asset['symbol'] == 'USDT'}
        fund_assets['USDT'] = cash
        return {symbol: quantity / units for symbol, quantity in fund_assets.items()}

    def init_fund_performance(self, history=120):
        snapshots = FundUnitSnapshot.objects.filter(fund=self).order_by('-age')
        if snapshots:
            return 'already exists'
        self._create_snapshots(
            assets=self.get_unit_assets(),
            # 'age': age,
            history=history
        )
        return 'created'

    def _create_snapshots(self, assets, history):
        historical = {}
        for asset in assets:
            if not asset == 'USDT':
                candles = requests.get('https://api.binance.com/api/v3/klines', params={  # TODO: cache to avoid request rate limit
                    'symbol': asset + 'USDT',
                    'interval': '1d',
                    'limit': 500
                }).json()
                historical[asset] = candles[-history - 5:-1]
            # else:
            #     historical[asset] = [1] * history
        age = 0
        while age <= history:
            age += 1
            portfo = {'age': history - age + 1, 'nav': max(assets['USDT'], 0)}
            for asset, quantity in assets.items():
                if not asset == 'USDT':
                    price = float(historical[asset][-age][4])
                    age_timestamp = int(historical[asset][-age][0] / 1000)
                    value = price * quantity
                    portfo[asset] = {
                        'value': value,
                        # 'timestamp': age_timestamp,
                    }
                    portfo['nav'] += value
                    portfo['date'] = timezone.datetime.fromtimestamp(age_timestamp).date()

            for asset, quantity in assets.items():
                if not asset == 'USDT':
                    portfo[asset]['ratio'] = portfo[asset]['value'] / portfo['nav']
                else:
                    # usdt_date = timezone.datetime.today() - timedelta(days=age-2)
                    portfo[asset] = {
                        'ratio': quantity / portfo['nav'],
                        'value': quantity,
                        # 'timestamp': usdt_date.timestamp(),
                        # 'date': usdt_date.date()
                    }
                if 'date' not in portfo:
                    usdt_date = timezone.datetime.today() - timedelta(days=age - 2)
                    portfo['date'] = usdt_date.date()
                FundUnitSnapshot(fund=self, asset=asset, quantity=quantity,
                                 value=portfo[asset]['value'],
                                 ratio=portfo[asset]['ratio'],
                                 insert_date=portfo['date'],
                                 age=portfo['age'], nav=portfo['nav']).save()
            # print(portfo)

    def fund_daily_snapshot(self):
        snapshot = FundUnitSnapshot.objects.filter(fund=self).order_by('-age').values('age', 'insert_date').first()
        insert_date = timezone.datetime.today()
        # print(snapshot['insert_date'], insert_date.date())
        if str(snapshot['insert_date']) == str(insert_date.date()):
            print('snapshot exists!')
            return None
        age = snapshot['age'] + 1  #TODO what if we miss a day?
        unit_assets = self.get_unit_assets()
        prices = oms.Binance.get_prices_for_nav(unit_assets)
        nav = sum([prices[asset] * quantity for asset, quantity in unit_assets.items()])
        for asset, quantity in unit_assets.items():
            value = quantity * prices[asset]
            ratio = value / nav
            FundUnitSnapshot(fund=self, asset=asset, quantity=quantity,
                             value=value,
                             ratio=ratio,
                             insert_date=insert_date,
                             age=age, nav=nav).save()

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

    def get_fund_performance(self, mode='all', history=120):
        snapshots = FundUnitSnapshot.objects.filter(fund=self).order_by('age').values('age', 'nav', 'insert_date')
        age = -1
        pnav = None
        result = []
        for snapshot in snapshots:
            if snapshot['age'] <= age:
                continue
            age += 1
            if pnav is None:
                pnav = snapshot['nav']
                continue
            r = (snapshot['nav'] / pnav) - 1
            pnav = snapshot['nav']
            result.append({
                'age': snapshot['age'],
                'nav': round(snapshot['nav'], 2),
                'date': snapshot['insert_date'],
                'return': 100 * round(r, 3)
            })
        result = result[-history:]
        if mode == 'fund':
            return [[int(1000 * time.mktime(r['date'].timetuple())), r['nav']] for r in result]
        btc_candles = requests.get('https://api.binance.com/api/v3/klines', params={
            'symbol': 'BTCUSDT',
            'interval': '1d',
            'limit': 500
        }).json()  # TODO: cache
        btc_prices = [float(c[4]) for c in btc_candles[-len(result) - 2:-1]]
        p_price = btc_prices[0]
        for idx, price in enumerate(btc_prices[1:]):
            result[idx]['btc'] = price
            result[idx]['btcReturn'] = 100 * round((price / p_price) - 1, 3)
            p_price = price
        if mode == 'btc':
            return [[int(1000 * time.mktime(r['date'].timetuple())), r['btc']] for r in result]
        return {'data': result[::-1]}


class FundInvestor(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    nationalCode = models.CharField(max_length=20, default='', blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, default='', blank=True, null=True)
    first_name = models.CharField(max_length=20, default='', blank=True, null=True)
    last_name = models.CharField(max_length=20, default='', blank=True, null=True)
    note = models.CharField(max_length=20, default='', blank=True, null=True)
    units = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


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
