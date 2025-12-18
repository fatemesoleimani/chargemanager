from rest_framework.viewsets import ModelViewSet

from apps.finance.models import ChargeRequest
from apps.finance.serializers.charge_request import SellerChargeRequestSerializer
from core.permission import IsSeller


class ChargeRequestViewSet(ModelViewSet):
    serializer_class = SellerChargeRequestSerializer
    permission_classes = [IsSeller]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return ChargeRequest.objects.filter(user=self.request.user).order_by("-created_at")
