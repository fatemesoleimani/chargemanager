from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.finance.choices import ChargeRequestStatusChoices
from apps.finance.exceptions import (
    ChargeRequestNotFound,
    ChargeRequestAlreadyProcessed,
)
from apps.finance.models import ChargeRequest
from apps.finance.services.wallet import WalletService
from apps.manager_admin.serializers.user_request import AdminChargeRequestActionSerializer
from core.permission import IsAdmin


class AdminChargeRequestActionView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(request=AdminChargeRequestActionSerializer, responses={200: dict},
                   description="Approve/Reject a seller charge request")
    @transaction.atomic
    def post(self, request, pk):
        serializer = AdminChargeRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        charge_request = ChargeRequest.objects.select_for_update().filter(pk=pk).first()
        if not charge_request:
            raise ChargeRequestNotFound()

        if charge_request.status != ChargeRequestStatusChoices.pending:
            raise ChargeRequestAlreadyProcessed()

        action = serializer.validated_data["action"]

        if action == "approve":
            WalletService.deposit(
                wallet=charge_request.user.wallet,
                amount=charge_request.amount,
            )
            charge_request.status = ChargeRequestStatusChoices.approved
        else:
            charge_request.status = ChargeRequestStatusChoices.rejected

        charge_request.approved_by = request.user
        charge_request.save(update_fields=["status", "approved_by"])

        return Response(
            {"detail": f"Charge request {action}d successfully."},
            status=status.HTTP_200_OK
        )
