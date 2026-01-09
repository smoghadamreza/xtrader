from django.contrib import admin

from sales.models import Package, Payment, Subscription


class PackAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        "price",
        "gas_fee",
        "days",
        "description",
    )


class SubsAdmin(admin.ModelAdmin):
    list_display = (
        "package",
        "user",
        "expiry",
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "amount",
        "reason",
        "insert_time",
        "txid",
    )


admin.site.register(Package, PackAdmin)
admin.site.register(Subscription, SubsAdmin)
admin.site.register(Payment, PaymentAdmin)
