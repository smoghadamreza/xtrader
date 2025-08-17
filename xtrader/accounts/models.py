import time
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models import OneToOneField
from django.template.loader import render_to_string
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

    def save(self, *args, **kwargs) -> None:
        self.user.username = self.user.username.lower()
        self.user.email = self.user.email.lower()
        self.user.save()
        if not self.referral_code:
            self.referral_code = self.user.username
        super().save(*args, **kwargs)

    def last_login(self) -> datetime|None:
        return self.user.last_login

    def first_name(self) -> str:
        return self.user.first_name

    def last_name(self) -> str:
        return self.user.last_name


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0, null=False, blank=False)
    income = models.FloatField(default=0, null=False, blank=False)
    address = models.CharField(
        max_length=80, default="", null=False, blank=False
    )
    nonce = models.CharField(max_length=40, default="", null=False, blank=False)
    last_change = models.IntegerField(default=lambda: int(time.time()), null=True, blank=True)

    def __str__(self):
        return self.user.username

class Deposit(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, null=True, blank=True
    )
    address_in = models.CharField(
        max_length=80, default="", null=False, blank=False
    )
    address_out = models.CharField(
        max_length=80, default="", null=False, blank=False
    )

    # tx: a widely known abbreviation for transaction
    txid_in = models.CharField(
        max_length=80, default="", null=False, blank=False
    )

    # tx: a widely known abbreviation for transaction
    txid_out = models.CharField(
        max_length=80, default="", null=False, blank=False
    )

    # The amount of USDT received by the deposit address. 
    init_amount = models.FloatField(default=0) 

    # the amount actually credited to the destination wallet (forwarded coin).
    # In other words: final_amount = init_amount - fees
    final_amount = models.FloatField(default=0)
    result = models.CharField(max_length=20, default="", null=True, blank=True)
    coin = models.CharField(max_length=10, default="", null=True, blank=True)
    network = models.CharField(
        max_length=10, default="", null=True, blank=True
    )

    # tx: a widely known abbreviation for transaction
    tx_time = models.DateTimeField(auto_now=True)
