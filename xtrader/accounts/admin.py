from django.contrib import admin
from .models import Profile, Wallet, Deposit
from userena.admin import UserenaAdmin
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'first_name', 'last_name', 'cellPhone', 'email', 'last_login', 'expire')

    def email(self, obj):
        return obj.user.email

    email.short_description = 'ایمیل'

    def make_published(self, request, queryset):
        print(queryset)


class DepositAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'coin', 'address_in', 'init_amount', 'final_amount', 'network',)


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'balance', 'nonce', 'last_change')



admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Deposit, DepositAdmin)
