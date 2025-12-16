from django.db import models


class TransactionTypeChoices(models.TextChoices):
    deposit = "Deposit", "واریز"
    withdraw = "Withdraw", "برداشت"


class ChargeRequestStatusChoices(models.TextChoices):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
