from django.db import models

from core.base_model import BaseModel


class Wallet(BaseModel):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} Wallet: {self.balance}"
