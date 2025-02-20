from django.contrib import admin
from .models import Profile, Wallet, Deposit


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'first_name', 'last_name', 'cellPhone', 'email', 'last_login', 'expire')

    # list_filter = ['gender','people_type','level_type','personwith','interstToCoaoprat']
    # ('user__first_name', 'user__last_name', 'user__username',)
    def email(self, obj):
        return obj.user.email

    email.short_description = 'ایمیل'

    def make_published(self, request, queryset):
        print(queryset)
        # return queryset.order_by('-user__last_login')
        # actions = [formfield_for_foreignkey]


# class SubscribeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'value', 'vip')

class DepositAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'coin', 'address_in', 'init_amount', 'final_amount', 'network',)


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'balance', 'nonce', 'last_change')


# class MembershipAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'subscribe', 'success')
# class MembershipAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'subscribe', 'success')


admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Deposit, DepositAdmin)
# admin.site.register(Membership, MembershipAdmin)
