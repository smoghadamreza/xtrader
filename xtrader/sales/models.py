from django.db import models
from django.contrib.auth.models import User
from accounts.models import Wallet, Profile
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class Package(models.Model):
    name = models.CharField(max_length=11, verbose_name='نام پکیج')
    category = models.CharField(max_length=11, null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    month_price = models.FloatField(default=0, null=True, blank=True)
    gas_fee = models.FloatField(default=0, null=True, blank=True)  #TODO: gas_fee?
    limit = models.FloatField(default=1, null=True, blank=True)
    days = models.IntegerField(default=30, null=True, blank=True)
    active = models.BooleanField(null=True)
    description = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name + str(self.price)

    def info(self):
        pack = {
            'id': self.id,
            'category': self.category,
            'price': self.price,
            'monthPrice': self.month_price,
            'name': self.name,
            'gasFee': self.gas_fee,
            'limit': self.limit,
            'days': self.days,
            'description': self.description,
        }
        return pack


class Subscription(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    expiry = models.DateTimeField(default=timezone.now, null=True, blank=True)

    @classmethod
    def have_subscribe(cls, user, packages='general'):  #TODO: it should have strict input type and return strict boolean
        if isinstance(packages, str):
            packages = [packages]
        subscription = Subscription.objects.filter(user=user, package__category__in=packages, expiry__gte=timezone.now()).order_by(
            '-package__gas_fee').first()
        return subscription

    def __str__(self):
        return self.package.name + self.user.username

    @classmethod
    def subscribe(cls, user, pack):
        wallet = Wallet.objects.filter(user=user).first()
        if not wallet:
            return {'s': 403, 'm': 'کیف پول یافت نشد'}
        if Subscription.have_subscribe(user):
            return {'s': 403, 'm': 'شما اشتراک دارید'}
        if wallet.balance < pack.price + 5:
            return {'s': 403, 'm': 'موجودی کیف پول کافی نیست (موجودی شما باید ۵ تتر بیشتر قیمت اشتراک باشد)'}
        expiry = timezone.now() + timedelta(days=pack.days + 2, hours=2)
        Subscription(package=pack, user=user, expiry=expiry).save()
        paid = Payment.pay(wallet=wallet, amount=pack.price, reason=f'خرید اشتراک {pack.name}', action='pay')
        if paid:
            return {'s': 200, 'm': 'خرید انجام شد'}
        return {'s': 403, 'm': 'موجودی کیف پول کافی نیست'}


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(default='', max_length=80, null=True, blank=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    reason = models.CharField(default='', max_length=500, null=True, blank=True)
    insert_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    txid = models.CharField(default='', max_length=100, null=True, blank=True)

    @classmethod
    def pay(cls, wallet, amount, action='pay', reason='', pay2ref=True, txid=''):
        ref_amount = round(amount * settings.REFERRAL_BOUNCE, 10)
        if action == 'pay':
            if wallet.balance < amount:
                return False
            wallet.balance -= amount
        elif action == 'income' and pay2ref:
            wallet.balance -= amount
            amount -= ref_amount
        else:
            wallet.income += amount
        wallet.save()
        Payment(user=wallet.user, amount=amount, action=action, reason=reason, txid=txid).save()
        if not pay2ref:
            return True
        referral_profile = Profile.objects.filter(user=wallet.user).first()
        if not referral_profile or not referral_profile.referred_by:
            return True
        Wallet.get_wallet(referral_profile.referred_by)
        referral_wallet = Wallet.objects.filter(user=referral_profile.referred_by).first()
        if referral_wallet:
            Payment.pay(wallet=referral_wallet,
                        amount=ref_amount,
                        action='receive',
                        reason='ریفرال',
                        pay2ref=False,
                        txid=txid,
                        )
        return True

