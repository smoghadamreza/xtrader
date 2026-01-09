from django.contrib import admin

from .models import Fund, FundInvestor, FundUnitSnapshot, UnitTransfer


class FundAdmin(admin.ModelAdmin):
    list_display = (
        "manager",
        "units",
        "aum",
        "fee",
        "last_update",
        "issue_fee",
        "redeem_fee",
    )

    def units(self, obj):
        return obj.get_units_count()


class FundInvestorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "fund",
        "units",
        "national_code",
        "phone_number",
        "note",
    )


class FundUnitSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "fund",
        "asset",
        "quantity",
        "value",
        "ratio",
        "insert_date",
        "nav",
        "age",
    )


class UnitTransferAdmin(admin.ModelAdmin):
    list_display = (
        "investor",
        "fund",
        "national_code",
        "action",
        "units",
        "nav",
        "value",
        "commission",
        "time",
    )

    def national_code(self, obj):
        return obj.investor.national_code

    def fund(self, obj):
        return obj.investor.fund


admin.site.register(Fund, FundAdmin)
admin.site.register(FundInvestor, FundInvestorAdmin)
admin.site.register(UnitTransfer, UnitTransferAdmin)
admin.site.register(FundUnitSnapshot, FundUnitSnapshotAdmin)
