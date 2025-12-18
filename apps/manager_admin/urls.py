from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from .views.approval_charge_request import AdminChargeRequestActionView
from .views.charge_request import AdminChargeRequestListView
from .views.transaction import AdminTransactionListView

router = DefaultRouter()
router.register("users", UserViewSet, basename="admin-users")

urlpatterns = [
    path(
        "charge_requests/",
        AdminChargeRequestListView.as_view(),
        name="admin-charge-request-list",
    ),
    path(
        "charge_requests/<int:pk>/action/",
        AdminChargeRequestActionView.as_view(),
        name="admin-charge-request-action",
    ),
    path(
        "transaction",
        AdminTransactionListView.as_view(),
        name="admin-transaction-list",
    ),
]
urlpatterns += router.urls
