from django.contrib import admin

from apps.finance.models import *


@admin.register(ChargeRequest)
class ChargeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "status",
        "approved_by",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("user", "amount", "created_at")

    ordering = ("-created_at",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("user", "balance", "created_at")

    ordering = ("-created_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "wallet",
        "amount",
        "type",
        "charge_target",
        "created_at",
    )
    list_filter = ("type", "created_at")
    search_fields = (
        "wallet__user__username",
        "charge_target",
    )
    readonly_fields = (
        "wallet",
        "amount",
        "type",
        "charge_target",
        "created_at",
    )

    ordering = ("-created_at",)
