from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from .views.approval_charge_request import AdminChargeRequestActionView
from .views.charge_request import AdminChargeRequestListView

router = DefaultRouter()
router.register("users", UserViewSet, basename="admin-users")

urlpatterns = [
    path("charge_requests/", AdminChargeRequestListView.as_view()),
    path("charge_requests/<int:pk>/action/", AdminChargeRequestActionView.as_view()),
]

urlpatterns += router.urls
