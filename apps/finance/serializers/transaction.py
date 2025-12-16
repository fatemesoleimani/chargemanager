from rest_framework import serializers

from apps.finance.models import Transaction


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "amount", "type", "charge_target", "created_at")
