from django.db import models

from apps.finance.choices import ChargeRequestStatusChoices
from core.base_model import BaseModel


class ChargeRequest(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=ChargeRequestStatusChoices.choices,
                              default=ChargeRequestStatusChoices.pending)
    approved_by = models.ForeignKey("user.User", null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="approved_requests")
