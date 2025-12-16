from rest_framework import serializers

from apps.finance.models import Transaction


class AdminTransactionListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="wallet.user.username")

    class Meta:
        model = Transaction
        fields = ("id", "amount", "type", "charge_target", "created_at", "username")
