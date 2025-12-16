from rest_framework import serializers


class SellerPhoneChargeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    amount = serializers.FloatField()

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
