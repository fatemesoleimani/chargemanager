from rest_framework import serializers

from apps.user.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "is_staff", "is_superuser", "is_active", "date_joined", "balance",)

    @staticmethod
    def get_balance(obj):
        wallet = getattr(obj, "wallet", None)
        if wallet:
            return wallet.balance
        return None
