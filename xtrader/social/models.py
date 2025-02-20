from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from accounts.models import Wallet
from sales.models import Payment
from django.conf import settings
from uuid import uuid4
from finance import oms

class Protrader(models.Model):  #TODO: Name should be camelCase
    trader = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    page_url = models.CharField(max_length=80, null=True, blank=True)
    page_kind = models.CharField(max_length=50, null=True, blank=True)
    brand = models.CharField(max_length=12, null=True, blank=True)
    subscription = models.FloatField(default=0, null=True, blank=True)

    age = models.IntegerField(null=True, blank=True)
    nav = models.IntegerField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    one_year_performance = models.FloatField(null=True, blank=True)
    six_months_performance = models.FloatField(null=True, blank=True)
    three_months_performance = models.FloatField(null=True, blank=True)
    one_months_performance = models.FloatField(null=True, blank=True)
    total_performance = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=12, null=True, blank=True)

    def create_pro(self, ex, ex_obj, brand=None, page_kind=None, page_url=None):
        public = ex_obj.public
        private = ex_obj.private
        return ex.get_historical_nav(public=public, private=private)  #TODO ????
        # nav = ex.get_last_nav(public=public, private=private)
        nav = 0
        # nav = navs[-1]
        # self.age = len(navs)
        self.age = 100
        self.nav = nav
        # self.one_year_performance = ((navs[-365][1] / self.nav) - 1) if self.age > 365 else None
        # self.six_months_performance = ((navs[-180][1] / self.nav) - 1) if self.age > 180 else None
        # self.three_months_performance = ((navs[-90][1] / self.nav) - 1) if self.age > 90 else None
        # self.one_months_performance = ((navs[-30][1] / self.nav) - 1) if self.age > 30 else None
        # self.total_performance = (navs[0][1] / self.nav) - 1
        self.brand = brand
        self.page_kind = page_kind
        self.page_url = page_url
        self.save()

    @staticmethod
    def get_history(trader):
        ex_obj, ex = oms.OMSManager.get_exchange(None, trader=trader)
        return ex.get_historical_nav(ex_obj.public, ex_obj.private)

    @staticmethod
    def get_records(trader):
        ex_obj, ex = oms.OMSManager.get_exchange(None, trader=trader)
        history = ex.get_historical_nav(ex_obj.public, ex_obj.private)
        records = {record['updateTime']: float(record['data']['totalAssetOfBtc']) for record in history}
        params = {"symbol": 'BTCUSDT', "interval": '1d', "limit": 50}
        candles = ex.get_candles(params)
        h = []
        btc = []
        for candle in candles:
            d = int(candle[6] / 1000)
            d *= 1000
            if d in records:
                h.append([d, round(records[d] * float(candle[4]), 2)])
                btc.append([d, round(float(candle[4]), 2)])
        return {'trader': h, 'btc': btc}

    @staticmethod
    def get_all(protrader_id=0):
        pros = Protrader.objects.filter(status='ACTIVE')
        result = []
        for pro in pros:
            result.append({
                'id': pro.id,
                'name': pro.brand,
                'pageKind': pro.page_kind,
                'link': pro.page_url,
                'subscription': pro.subscription,
                'age': pro.age,
                'nav': pro.nav,
                'beta': pro.beta,
                'one_year_performance': pro.one_year_performance,
                'six_months_performance': pro.six_months_performance,
                'three_months_performance': pro.three_months_performance,
                'one_months_performance': pro.one_months_performance,
                'total_performance': pro.total_performance,
                'protrader_id': protrader_id,  #TODO ??????
            })
        return result

    def copy_order(self, new_order):
        followings = Follow.objects.filter(proTrader=self, expiry__gte=timezone.now())
        if not followings:
            return 0  #TODO: why?. if it is status code, why there isn't a success status code to return after the following line?
        oms.OMSManager.copytrade(trader=self.trader, new_order=new_order, followers=followings)


class Follow(models.Model):
    proTrader = models.ForeignKey(Protrader, null=True, blank=True, on_delete=models.CASCADE)
    follower =   models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    expiry = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def subscribe(self, period=32):
        self.expiry += timedelta(days=period)
        follower_wallet = Wallet.objects.filter(user=self.follower).first()
        fee = self.proTrader.subscription
        if not follower_wallet or follower_wallet.balance < fee:
            return False
        Wallet.get_wallet(self.proTrader.trader)
        trader_wallet = Wallet.objects.filter(user=self.proTrader.trader).first()
        if not trader_wallet:
            return False

        site_fee = round(fee * settings.COPYTRADEFEE, 3)
        trader_fee = round(fee - site_fee, 3)
        txid = str(uuid4())
        Payment.pay(wallet=follower_wallet, amount=site_fee, action='income', reason=self.proTrader.brand, pay2ref=True,
                    txid=txid)
        Payment.pay(wallet=follower_wallet, amount=trader_fee, action='pay', reason=self.proTrader.brand, pay2ref=False,
                    txid=txid)
        Payment.pay(wallet=trader_wallet, amount=trader_fee, action='receive',
                    reason='copyTrading-' + str(follower_wallet.id), pay2ref=False, txid=txid)
        return True

    @staticmethod
    def copytrade(user, brand, action):
        if Protrader.objects.filter(trader=user).first():
            action = -1
        following = Follow.objects.filter(proTrader__brand=brand, follower=user).first()
        if action == 1:  # follow
            if not following:
                if Follow.objects.filter(follower=user).first():
                    result = {'c': 403, 'msg': 'شما تریدر دیگری را دنبال می‌کنید'}
                else:
                    protrader = Protrader.objects.filter(brand=brand, status='ACTIVE').first()
                    if protrader:
                        follow = Follow(proTrader=protrader, follower=user)
                        if follow.subscribe():
                            follow.save()
                            result = {'c': 200}
                        else:
                            result = {'c': 302, 'msg': 'موجودی شما کافی نیست', 'href': '/profile/setup/?s=wallet'}
                    else:
                        result = {'c': 403, 'msg': 'تریدر یافت نشد'}
            else:
                result = {'c': 403, 'msg': 'شما قبلا این تریدر را دنبال کردید'}
        elif action == 0:  # unfollow
            if following:
                following.unfollow()
                result = {'c': 200}
            else:
                result = {'c': 403, 'msg': 'شما قبلا این تریدر را دنبال نکردید'}
        elif action == -1:
            result = {'c': 403, 'msg': 'شما مجاز به دنبال کردن نیستید!'}
        else:
            result = {'c': 403, 'msg': 'مقدار action اشتباه است'}
        return result

    def unfollow(self):
        self.delete()


class TraderHistory(models.Model):
    trader = models.ForeignKey(Protrader, on_delete=models.CASCADE)
    record_time = models.IntegerField(default=0, null=True, blank=True)
    btc = models.FloatField(default=0, null=True, blank=True)
    nav = models.FloatField(default=0, null=True, blank=True)
