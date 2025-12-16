from django.db import models

from apps.finance.choices import TransactionTypeChoices
from core.base_model import BaseModel


class Transaction(BaseModel):
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE, related_name="transactions")
    amount = models.FloatField()
    type = models.CharField(max_length=10, choices=TransactionTypeChoices.choices)
    charge_target = models.CharField(max_length=255)
