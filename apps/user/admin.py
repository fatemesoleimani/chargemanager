from django.contrib import admin

from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "is_superuser",
        "wallet_balance",
        "is_active",
        "date_joined",
    )

    def wallet_balance(self, obj):
        if hasattr(obj, "wallet"):
            return obj.wallet.balance
        return None

    wallet_balance.short_description = "Balance"
