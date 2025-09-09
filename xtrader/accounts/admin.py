from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from .models import Deposit, Profile, Wallet


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "first_name",
        "last_name",
        "cellPhone",
        "email",
        "last_login",
        "expire",
    )

    @admin.display(description="ایمیل")
    def email(self, obj):
        return obj.user.email

    def make_published(self, request, queryset):
        print(queryset)


class DepositAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "coin",
        "address_in",
        "init_amount",
        "final_amount",
        "network",
    )


class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "balance", "nonce", "updated_at")


admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Deposit, DepositAdmin)
