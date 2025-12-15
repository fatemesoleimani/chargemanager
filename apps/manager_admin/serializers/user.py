from rest_framework import serializers

from apps.finance.models.wallet import Wallet
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "is_staff", "is_superuser", "is_active", "date_joined", "balance")
        read_only_fields = ("id", "date_joined", "is_staff", "is_active", "balance")

    @staticmethod
    def get_balance(obj):
        if hasattr(obj, "wallet") and obj.wallet:
            return obj.wallet.balance
        return None

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        if not user.is_superuser:
            Wallet.objects.get_or_create(user=user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if not instance.is_superuser:
            Wallet.objects.get_or_create(user=instance)
        return instance
