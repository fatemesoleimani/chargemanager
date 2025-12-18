from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.finance.views import *
from apps.finance.views.charge_sale import SellerPhoneChargeView
from apps.finance.views.transaction import TransactionListView

router = DefaultRouter()
router.register("charge_requests", ChargeRequestViewSet, basename="seller-charge-request")

urlpatterns = [
    path("transaction", TransactionListView.as_view(),name="transaction-list"),
    path("charge_phone", SellerPhoneChargeView.as_view()),
]

urlpatterns += router.urls
