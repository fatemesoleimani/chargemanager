from rest_framework.routers import DefaultRouter

from apps.finance.views import *

router = DefaultRouter()
router.register("charge_requests", ChargeRequestViewSet, basename="seller-charge-request")

urlpatterns = router.urls
