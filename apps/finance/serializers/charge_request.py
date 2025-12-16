from rest_framework import serializers

from apps.finance.models import ChargeRequest


class SellerChargeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeRequest
        fields = ("id", "amount", "status", "created_at")
        read_only_fields = ("id", "status", "created_at")

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return ChargeRequest.objects.create(user=user, amount=validated_data["amount"])
