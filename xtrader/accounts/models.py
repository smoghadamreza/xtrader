import random
import string
import time
from uuid import uuid4

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models import OneToOneField
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from userena.models import UserenaBaseProfile


class Profile(UserenaBaseProfile):
    user = OneToOneField(
        User,
        unique=True,
        verbose_name=_("user"),
        related_name="my_profile",
        on_delete=models.CASCADE,
    )
    cellPhone = models.CharField(
        max_length=20, verbose_name="شماره تلفن ", null=True, blank=True
    )
    expire = models.DateField(null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True)
    telegram_activation_code = models.CharField(
        max_length=12, null=True, blank=True
    )
    telegram_activation_timestamp = models.IntegerField(null=True, blank=True)
    referral_code = models.CharField(
        default="", max_length=80, blank=True, null=True
    )
    referred_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.user.username = self.user.username.lower()
        self.user.email = self.user.email.lower()
        self.user.save()
        if not self.referral_code:
            self.referral_code = self.user.username
        super().save(*args, **kwargs)

    @classmethod
    def make_referral_codes(cls):
        pros = cls.objects.all()
        for pro in pros:
            if not pro.referral_code:
                pro.referral_code = pro.user.username
                pro.save()

    @classmethod
    def make_lowercase(cls):
        pros = cls.objects.all()
        for pro in pros:
            user = pro.user
            if user.username:
                user.username = user.username.lower()
            if user.email:
                user.email = user.email.lower()
            user.save()

    @staticmethod
    def code_generator(size=6):
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(size))

    def get_code(self) -> str:
        t = int(time.time())
        if (
            self.telegram_activation_code
            and self.telegram_activation_timestamp
            and self.telegram_activation_timestamp > t
        ):
            return self.telegram_activation_code

        code = Profile.code_generator()
        self.telegram_activation_timestamp = t + (5 * 60)
        self.telegram_activation_code = code
        self.save()
        return code

    def last_login(self):
        return self.user.last_login

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    @classmethod
    def mail_users(cls, subject, emails=None):
        if not emails:
            emails = []
            pros = cls.objects.all()
            for pro in pros:
                email = pro.user.email
                if email and pro.user.is_active:
                    emails.append(email)
        failed_emails = []
        for email in emails:
            try:
                html_message = render_to_string(
                    "mail_template.html", {"context": "values"}
                )
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to = email
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    [to],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception:
                failed_emails.append(email)
        print("failed:", failed_emails)
        return failed_emails


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0, null=False, blank=False)
    income = models.FloatField(default=0, null=True, blank=True)
    address = models.CharField(
        max_length=80, default="", null=True, blank=True
    )
    nonce = models.CharField(max_length=40, default="", null=True, blank=True)
    last_change = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_gateway_base():
        return "https://api.cryptapi.io"

    @classmethod
    def get_wallet(cls, user):
        wallet = cls.objects.filter(user=user).first()
        income = 0
        if wallet:
            balance = wallet.balance
            income = wallet.income
            if wallet._should_regenerate_address:
                address = wallet.create_address()
            else:
                address = wallet.address
        else:
            wallet = cls(user=user)
            address = wallet.create_address()
            balance = wallet.balance
        return {
            "address": address,
            "balance": round(balance, 6),
            "income": income,
        }

    def create_address(self, num=0):
        if num > 3:
            return ""
        self.nonce = str(uuid4())
        params = {
            "address": settings.USDT_WALLET,
            "callback": settings.SITE_ADDRESS
            + "/accounts/new-deposit/"
            + "?nonce={}".format(self.nonce),
            "priority": "economic",
            "post": 1,
        }
        response = requests.get(
            Wallet.get_gateway_base() + "/trc20/usdt/create", params=params
        ).json()
        if "status" in response and response["status"] == "success":
            self.address = response["address_in"]
            self.save()
            return self.address
        else:
            time.sleep(1)
            return self.create_address(num=num + 1)

    def check_deposit(self):
        params = {
            "callback": settings.SITE_ADDRESS
            + "/accounts/new-deposit/"
            + "?nonce={}".format(self.nonce),
        }
        logs = requests.get(
            Wallet.get_gateway_base() + "/trc20/usdt/logs", params=params
        ).json()
        new_deposit = False
        for callback in logs["callbacks"]:
            depo = Deposit.objects.filter(txid_in=callback["txid_in"]).first()
            if depo:
                continue
            new_deposit = True
            params = {
                "address_in": logs["address_in"],
                "address_out": logs["address_out"],
                "txid_in": callback["txid_in"],
                "txid_out": callback["txid_out"],
                "value_coin": callback["value_coin"],
                "value_forwarded_coin": callback["value_forwarded_coin"],
                "coin": "trc20_usdt",
                "result": callback["result"],
            }
            Deposit.create(nonce=self.nonce, params=params, wallet=self)
        return new_deposit

    @property
    def _should_regenerate_address(self) -> bool:
        """Check if address is older than 70 days."""
        return (timezone.now() - self.last_change).days > 70


class Deposit(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, null=True, blank=True
    )
    address_in = models.CharField(
        max_length=80, default="", null=True, blank=True
    )
    address_out = models.CharField(
        max_length=80, default="", null=True, blank=True
    )
    txid_in = models.CharField(
        max_length=80, default="", null=True, blank=True
    )
    txid_out = models.CharField(
        max_length=80, default="", null=True, blank=True
    )
    init_amount = models.FloatField(default=0, null=True, blank=True)
    final_amount = models.FloatField(default=0, null=True, blank=True)
    result = models.CharField(max_length=20, default="", null=True, blank=True)
    coin = models.CharField(max_length=10, default="", null=True, blank=True)
    network = models.CharField(
        max_length=10, default="", null=True, blank=True
    )
    tx_time = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, nonce, params, wallet=None):
        address_in = params["address_in"]
        amount = float(params["value_coin"])
        final_amount = float(params["value_forwarded_coin"])
        network, coin = params["coin"].split("_")
        if cls.objects.filter(
            address_in=address_in, txid_in=params["txid_in"]
        ):
            return False
        if wallet is None:
            wallet = Wallet.objects.filter(
                nonce=nonce, address=address_in
            ).first()
        deposit = cls(
            wallet=wallet,
            address_in=params["address_in"],
            address_out=params["address_out"],
            txid_in=params["txid_in"],
            txid_out=params["txid_out"],
            init_amount=amount,
            final_amount=final_amount,
            result=params["result"],
            coin=coin,
            network=network,
        )
        deposit.save()
        if wallet:
            wallet.balance += amount
            wallet.save()
        return True

    @classmethod
    def get_deposits(cls, wallet=None):
        deposits = cls.objects.filter(wallet=wallet).order_by("tx_time")
        result = []
        for deposit in deposits:
            result.append(
                {
                    "amount": deposit.init_amount,
                    "txid": deposit.txid_in,
                    "action": "واریز",
                    "coin": "تتر (trc20)",
                    "time": str(
                        deposit.tx_time,
                    ).replace("T", " "),
                    "id": deposit.pk,
                }
            )
        return result

    def pay2referral(self, amount):
        pass
