from rest_framework.generics import ListAPIView

from apps.finance.models import ChargeRequest
from apps.manager_admin.serializers.user_request import AdminChargeRequestListSerializer
from core.permission import IsAdmin


class AdminChargeRequestListView(ListAPIView):
    serializer_class = AdminChargeRequestListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return ChargeRequest.objects.all().order_by("-created_at")
