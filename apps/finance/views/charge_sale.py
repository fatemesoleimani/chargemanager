from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.finance.serializers.charge_sale import SellerPhoneChargeSerializer
from apps.finance.services.wallet import WalletService
from core.permission import IsSeller


class SellerPhoneChargeView(APIView):
    permission_classes = [IsSeller]

    @extend_schema(
        request=SellerPhoneChargeSerializer,
        responses={200: dict},
        description="Seller charges a phone number and wallet balance is reduced"
    )
    @transaction.atomic
    def post(self, request):
        serializer = SellerPhoneChargeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        amount = serializer.validated_data["amount"]

        try:
            WalletService.withdraw(
                wallet=request.user.wallet,
                amount=amount,
                reference=phone_number,
            )
        except ValueError:
            return Response(
                {"detail": "Insufficient balance."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Phone charged successfully."},
            status=status.HTTP_200_OK
        )
