from rest_framework.generics import ListAPIView

from apps.finance.models import Transaction
from apps.manager_admin.serializers.transaction import AdminTransactionListSerializer
from core.permission import IsAdmin


class AdminTransactionListView(ListAPIView):
    serializer_class = AdminTransactionListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Transaction.objects.all().order_by("-created_at")
