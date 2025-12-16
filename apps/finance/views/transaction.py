from rest_framework.generics import ListAPIView

from apps.finance.models import Transaction
from apps.finance.serializers.transaction import TransactionListSerializer
from core.permission import IsSeller


class TransactionListView(ListAPIView):
    serializer_class = TransactionListSerializer
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Transaction.objects.all().order_by("-created_at")
