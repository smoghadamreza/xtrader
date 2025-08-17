from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from accounts.models import Wallet
from sales.models import Payment


class ProTrader(models.Model):
    trader = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    page_url = models.CharField(max_length=80, null=True, blank=True)
    page_kind = models.CharField(max_length=50, null=True, blank=True)
    brand = models.CharField(max_length=12, null=False, blank=True)
    subscription = models.FloatField(default=0, null=False, blank=True)

    age = models.IntegerField(null=True, blank=True)
    nav = models.IntegerField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    one_year_performance = models.FloatField(null=True, blank=True)
    six_months_performance = models.FloatField(null=True, blank=True)
    three_months_performance = models.FloatField(null=True, blank=True)
    one_months_performance = models.FloatField(null=True, blank=True)
    total_performance = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=12, null=True, blank=True)

    @staticmethod
    def get_all(protrader_id=0):
        pros = ProTrader.objects.filter(status="ACTIVE")
        result = []
        for pro in pros:
            result.append(
                {
                    "id": pro.pk,
                    "name": pro.brand,
                    "pageKind": pro.page_kind,
                    "link": pro.page_url,
                    "subscription": pro.subscription,
                    "age": pro.age,
                    "nav": pro.nav,
                    "beta": pro.beta,
                    "one_year_performance": pro.one_year_performance,
                    "six_months_performance": pro.six_months_performance,
                    "three_months_performance": pro.three_months_performance,
                    "one_months_performance": pro.one_months_performance,
                    "total_performance": pro.total_performance,
                    "protrader_id": protrader_id,
                }
            )
        return result


class Follow(models.Model):
    pro_trader = models.ForeignKey(
        ProTrader, null=False, blank=True, on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    expiry = models.DateTimeField(null=False, blank=False)

    def subscribe(self, period=32):
        self.expiry += timedelta(days=period)
        follower_wallet = Wallet.objects.filter(user=self.follower).first()
        if follower_wallet is None:
            raise ValueError("user Wallet was not found")
        fee = self.pro_trader.subscription
        if not follower_wallet or follower_wallet.balance < fee:
            return False
        Wallet.get_wallet(self.pro_trader.trader)
        trader_wallet = Wallet.objects.filter(
            user=self.pro_trader.trader
        ).first()
        if not trader_wallet:
            return False

        site_fee = round(fee * settings.COPYTRADEFEE, 3)
        trader_fee = round(fee - site_fee, 3)
        txid = str(uuid4())
        Payment.pay(
            wallet=follower_wallet,
            amount=site_fee,
            action="income",
            reason=self.pro_trader.brand,
            pay2ref=True,
            txid=txid,
        )
        Payment.pay(
            wallet=follower_wallet,
            amount=trader_fee,
            action="pay",
            reason=self.pro_trader.brand,
            pay2ref=False,
            txid=txid,
        )
        Payment.pay(
            wallet=trader_wallet,
            amount=trader_fee,
            action="receive",
            reason="copyTrading-" + str(follower_wallet.pk),
            pay2ref=False,
            txid=txid,
        )
        return True

    @staticmethod
    def copy_trade(user, brand, action):
        if ProTrader.objects.filter(trader=user).first():
            action = -1
        following = Follow.objects.filter(
            proTrader__brand=brand, follower=user
        ).first()
        if action == 1:  # follow
            if not following:
                if Follow.objects.filter(follower=user).first():
                    result = {
                        "c": 403,
                        "msg": "شما تریدر دیگری را دنبال می‌کنید",
                    }
                else:
                    protrader = ProTrader.objects.filter(
                        brand=brand, status="ACTIVE"
                    ).first()
                    if protrader:
                        follow = Follow(proTrader=protrader, follower=user)
                        if follow.subscribe():
                            follow.save()
                            result = {"c": 200}
                        else:
                            result = {
                                "c": 302,
                                "msg": "موجودی شما کافی نیست",
                                "href": "/profile-setup/?s=wallet",
                            }
                    else:
                        result = {"c": 403, "msg": "تریدر یافت نشد"}
            else:
                result = {"c": 403, "msg": "شما قبلا این تریدر را دنبال کردید"}
        elif action == 0:  # unfollow
            if following:
                following.unfollow()
                result = {"c": 200}
            else:
                result = {
                    "c": 403,
                    "msg": "شما قبلا این تریدر را دنبال نکردید",
                }
        elif action == -1:
            result = {"c": 403, "msg": "شما مجاز به دنبال کردن نیستید!"}
        else:
            result = {"c": 403, "msg": "مقدار action اشتباه است"}
        return result

    def unfollow(self):
        self.delete()


class TraderHistory(models.Model):
    trader = models.ForeignKey(ProTrader, on_delete=models.CASCADE)
    record_time = models.IntegerField(default=0, null=True, blank=True)
    btc = models.FloatField(default=0, null=True, blank=True)
    nav = models.FloatField(default=0, null=True, blank=True)
