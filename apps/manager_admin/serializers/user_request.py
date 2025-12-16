from rest_framework import serializers

from apps.finance.models import ChargeRequest


class AdminChargeRequestListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ChargeRequest
        fields = ("id", "username", "amount", "status", "created_at",)


class AdminChargeRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approve", "reject"])
